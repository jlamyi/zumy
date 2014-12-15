import time, threading, serial
from numpy import *
from Xbee import XbRssi

class Xbee_chaining_bot(XbRssi):
    def __init__(self,serial_port): 
        XbRssi.__init__(self,serial_port)        
        self.predecessor = 0
        self.successor = 0
        self.ascend = False
        self.descend = False
        self.startReceive = True
        self.goingSentry = False
        self.cmdList = []
        self.safeModeCounter = 0

    def receive_loop(self):
        while True:

            self.response = self.xbee.wait_read_frame()
            self.rssi = -ord(self.response.get('rssi'))
            self.addr = ord(self.response.get('source_addr')[1])
            self.data = self.response.get('rf_data')

            self.decode_msg() 

    def decode_msg(self):
        if (self.response != 0):
            msg =  self.get_command(self.data)
            print msg
            if msg.endswith('TRANSMIT_START'):
                if (self.predecessor == self.get_sender_id(msg)):
                    self.transmit = True
                    self.sendingCommand = True
                    print "BUG"
                    self.cmdList.append('ASCEND_START')

            elif msg.endswith('TRANSMIT_STOP'):
                print 'Setting transmit flag to false'
                self.transmit = False 

            elif msg.endswith('ASCEND_START'):
                self.ascend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK_ASCEND_START'

            elif msg.endswith('DESCEND_START'):
                self.descend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK_DESCEND_START'

            elif msg.endswith('ARRIVAL'):
                self.sendingCommand = True
                self.sendMessage = 'ACK_ARRIVAL'
                self.goingSentry = True
                #self.cmdList.append('TRANSMIT_START')
                if (self.successor == 0):
                    self.successor = self.get_sender_id(msg)
                    print 'Successor is set to'+str(self.successor)
                    self.cmdList.append('SET_PREDECESSOR')
                #self.cmdList.append('ASCEND_START')

            elif msg.endswith('SET_PRED'):
                print 'in set pred'
                self.set_predecessor(msg)
                self.sendMessage = 'ACK_SET_PREDECESSOR'
                self.sendingCommand = True

            elif msg.endswith('STOP_ACK'):
                self.sendingCommand = False

            elif 'ACK' in msg:
                print "ACKED"
                self.sendingCommand = True
                self.sendMessage = 'STOP_ACK'  
                
            else:
                if self.sendMessage.endswith('STOP_ACK'):
                    self.sendingCommand = False
                if self.sendMessage.isdigit() and msg.isdigit():
                    print "regular transmission"
                    if self.sendingCommand == False:
                        safe = False
                        if (safeModeCounter == 0):
                            safeModeCounter = int(self.sendMessage)
                        else:
                            if (safeModeCounter - int(self.sendMessage)) > 0: 
                                safe = True
                                safeModeCounter = 0
                        if (safe):
                            if len(self.cmdList):
                                print "COMMAND LIST FUNCTION"
                                print self.cmdList
                                self.send_signal(self.cmdList.pop())
                            else:
                                if self.goingSentry == True:
                                    self.transmit = False
        else:
            return 0

    def send_signal(self, msg):
        self.sendMessage = msg
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
            self.predecessor = int(self.get_sender_id(msg))
            print 'Predecessor is set to'+str(self.predecessor)

    def chain_next_bot(self, msg):
        self.send_start_transmit_signal()
        if (self.successor == 0):
            self.successor = self.get_sender_id(msg)
            print 'Successor is set to'+str(self.successor)
            self.send_set_predecessor_signal()
        self.send_start_ascend_signal()
        self.transmit = False

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

