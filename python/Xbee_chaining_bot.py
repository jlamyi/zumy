import time, threading, serial
from numpy import *
from Xbee import XbRssi

class Xbee_chaining_bot(XbRssi):
    def __init__(self,serial_port): 
        XbRssi.__init__(self,serial_port)        
        self.predecessor = 0
        self.successor = 0
        self.transmit = True
        self.ascend = False
        self.descend = False
        self.startReceive = True
        self.sendMessage = self.id+'PKT'
        self.cmdList = []

    def receive_loop(self):
        while True:

            self.response = self.xbee.wait_read_frame()
            self.rssi = -ord(self.response.get('rssi'))
            self.addr = ord(self.response.get('source_addr')[1])
            self.data = self.response.get('rf_data')

            self.decode_msg() 

    def decode_msg(self):
        if (self.response != 0):
            msg =  self.data
            print msg
            if msg.startswith('TRANSMIT_START'):
                if (self.predecessor == self.get_sender_id(msg)):
                    self.transmit = True
                    self.sendingCommand = True

            elif msg.startswith('TRANSMIT_STOP'):
                print 'Setting transmit flag to false'
                self.transmit = False 

            elif msg.startswith('ASCEND_START'):
                self.ascend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK_ASCEND_START'+str(self.rid)

            elif msg.startswith('DESCEND_START'):
                self.descend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK_DESCEND_START'+str(self.rid)

            elif msg.startswith('ARRIVAL'):
                self.sendingCommand = True
                self.sendMessage = 'ACK_ARRIVAL'+str(self.rid)
                self.cmdList.append('TRANSMIT_START')
                if (self.successor == 0):
                    self.successor = self.get_sender_id(msg)
                    print 'Successor is set to'+str(self.successor)
                    self.cmdList.append('SET_PREDECESSOR')
                self.cmdList.append('ASCEND_START')

            elif msg.startswith('SET_PREDECESSOR'):
                self.set_predecessor(msg)
                self.sendMessage = 'ACK_SET_PREDECESSOR'+str(self.rid)
                self.sendingCommand = True

            elif msg.startswith('ACK'):
                self.sendingCommand = True
                self.sendMessage = 'STOP_ACK'+str(self.rid)  

            elif msg.startswith('STOP_ACK'):
                self.sendingCommand = False
                
            else:
                if self.sendMessage.startswith('STOP_ACK'):
                    self.sendingCommand = False
                if self.sendMessage.isdigit() and msg.isdigit():
                    print "regular transmission"
                    if len(self.cmdList):
                        self.send_signal(self.cmdList.pop())
        else:
            return 0

    def send_signal(self, msg):
        self.sendMessage = msg + '-'+str(self.rid)
        self.sendingCommand = True
        while(self.sendingCommand == True):
            print self.data
            print 'waiting_ack_for_'+msg
            time.sleep(3)

    def send_arrival_signal(self):
        self.send_signal('ARRIVAL')

    def send_start_transmit_signal(self):
        self.send_signal('TRANSMIT_START')

    def send_stop_transmit_signal(self):
        self.send_signal('TRANSMIT_STOP')

    def send_set_predecessor_signal(self):
        self.send_signal('SET_PREDECESSOR') 

    def send_start_ascend_signal(self):
        self.send_signal('ASCEND_START')

    def end_gradient_ascend(self):
        self.ascend = False
        self.send_arrival_signal()

    def set_predecessor(self, msg):
        if (self.predecessor == 0):
            self.predecessor = self.get_sender_id(msg)
            print 'Predecessor is set to'+str(self.predecessor)

    def chain_next_bot(self, msg):
        self.send_start_transmit_signal()
        if (self.successor == 0):
            self.successor = self.get_sender_id(msg)
            print 'Successor is set to'+str(self.successor)
            self.send_set_predecessor_signal()
        self.send_start_ascend_signal()
        self.transmit = False

    def get_sender_id(self, msg):
        start_index = msg.index('-')
        return msg[start_index:]

if __name__=='__main__':
    xb = Xbee_chiaing_bot('/dev/ttyUSB0')

    result = xb.get_max_rssi()
    print "the maximum is: ", result
    result = xb.get_min_rssi()
    print "the minimum is: ", result
    result = xb.get_avg_rssi()
    print "the average is: ", result
    result = xb.get_med_rssi()
    print "the median is: ", result

