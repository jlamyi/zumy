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
        self.cmdHist = []
        self.safeModeCounter = 0
        self.startCommandPkt = 0

    def receive_loop(self):
        while True:

            self.response = self.xbee.wait_read_frame()
            self.rssi = -ord(self.response.get('rssi'))
            self.addr = ord(self.response.get('source_addr')[1])
            self.data = self.response.get('rf_data')

            self.decode_msg() 

    def decode_msg(self):
        if (self.response != 0):
            msg = self.data
            self.cmdHist.append(msg)
            msg =  self.get_command(self.data)
            print msg
            print self.cmdHist
            if msg.startswith('TRANSMIT_START'):
                if (self.predecessor == self.get_sender_id(msg)):
                    self.transmit = True
                    self.sendingCommand = True
                    print "BUG"
                    self.cmdList.append('ASCEND_START')

            elif msg.startswith('TRANSMIT_STOP'):
                print 'Setting transmit flag to false'
                self.transmit = False 

            elif msg.startswith('ASCEND_START'):
                self.ascend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK_ASCEND_START'

            elif msg.startswith('DESCEND_START'):
                self.descend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK_DESCEND_START'

            elif msg.startswith('ARRIVAL'):
                self.sendingCommand = True
                self.sendMessage = 'ACK_ARRIVAL'
                self.goingSentry = True
                
                if (self.successor == 0):
                    self.successor = self.get_sender_id(msg)
                    print 'Successor is set to'+str(self.successor)
                    self.cmdList.append('SET_PREDECESSOR')
                else:
                    self.cmdList.append('TRANSMIT_START')

                self.cmdList.append('ASCEND_START')

            elif msg.startswith('SET_PRED'):
                print 'in set pred'
                self.set_predecessor(msg)
                self.sendMessage = 'ACK_SET_PREDECESSOR'
                self.sendingCommand = True

            elif msg.startswith('STOP_ACK'):
                self.sendingCommand = False
                self.sendMessage = ''

            elif msg.startswith('ACK'):
                self.sendingCommand = True
                self.sendMessage = 'STOP_ACK'  
                self.startCommandPkt = self.pktNum
                
            else:
                if self.sendMessage.startswith('STOP_ACK'):
                    if self.pktNum > self.startCommandPkt+2:
                        print "End cycle"
                        self.sendingCommand = False
                        self.sendMessage = ''

                if (len(self.sendMessage) == 0 and len(msg) == 0):
                    print "regular transmission"
                    if self.sendingCommand == False:

                        safe = False
                        if (self.safeModeCounter == 0):
                            print 'set safe counter'
                            print self.cmdList
                            self.safeModeCounter = self.pktNum
                        else:
                            if (int(self.pktNum) - self.safeModeCounter) > 3: 
                                print 'safe for next command'
                                safe = True
                                self.safeModeCounter = 0
                        if (safe):
                            if len(self.cmdList):
                                print "COMMAND LIST FUNCTION"
                                print self.cmdList
                                self.sendMessage = self.cmdList.pop()
                                self.sendingCommand = True
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

    def send_change_channel_signal(self):
        self.send_signal('CHANGE_CHANNEL')

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

