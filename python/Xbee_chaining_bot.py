
import time, threading, serial, zc_id
#from xbee import XBee
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

    def receive_loop(self):
        while True:
            #if self.startReceive == True:
            # self.get_max_rssi()
            #self.receive_pkt()

            self.response = self.xbee.wait_read_frame()
            self.rssi = -ord(self.response.get('rssi'))
            self.addr = ord(self.response.get('source_addr')[1])
            self.data = self.response.get('rf_data')

            self.decode_msg() 
            #time.sleep(10)

    def decode_msg(self):
        if (self.response != 0):
            msg =  self.data
            print msg
            if msg.startswith('TRANSMIT_START'):
                if (self.predecessor == self.get_sender_id(msg)):
                    self.transmit = True
                    self.send_ack()
                    #self.sendMessage = 'ACK_TRANSMIT_START'
            elif msg.startswith('TRANSMIT_STOP'):
                print 'Setting transmit flag to false'
                self.transmit = False               
            elif msg.startswith('ASCEND_START'):
                self.ascend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK'                
            elif msg.startswith('DESCEND_START'):
                self.descend = True
                self.sendingCommand = True
                self.sendMessage = 'ACK'
            elif msg.startswith('ARRIVAL'):
                self.sendingCommand = True
                self.sendMessage = 'ACK'
            elif msg.startswith('SET_PREDECESSOR'):
                self.set_predecessor(msg)
                self.sendMessage = 'ACK_SET_PREDECESSOR'
                self.send_ack()
            elif msg.startswith('ACK'):
                self.sendingCommand = True
                self.sendMessage = 'STOP_ACK'           
            elif msg.startswith('STOP_ACK'):
                self.sendingCommand = False
            else:
                if self.sendMessage.startswith('STOP_ACK'):
                    self.sendingCommand = False

        else:
            return 0

    def send_ack(self):
        send_msg = 'ACK'+str(self.rid)
        msg = self.data
        strr='0'
        while(~msg.startswith('STOP_ACK')):
            print "Sending ACK"
            self.xbee.tx(dest_addr='\xFF\xFF', data = send_msg)
            self.pktNum = self.pktNum + 1
            msg = self.data
            i = 0
            while True:
                i = i+1
                #try:
                #    signal.signal(signal.SIGALRM, self.read_byte()) 
                #    signal.alarm(10)
                cur_char = str(self.ser.read())

                strr = strr+ cur_char
                #except:
                #    break
                #strr = strr+ str(self.ser.read())
                if i > 20:
                    break
                if 'STOP' in strr:
                    break
                print strr 
            print 'msg:' + msg
            if 'STOP' in strr:
                break
            self.ser.flush()
            strr = '0'
            time.sleep(3)
        self.sendMessage = ''.join(['Hello #', repr(self.pktNum)] )
        send_msg = self.sendMessage
        strr='0'

        while(~msg.startswith('Hello')):
            print "Sending Ending_command"
            self.xbee.tx(dest_addr='\xFF\xFF', data = send_msg)
            self.pktNum = self.pktNum + 1
            msg = self.data
            i = 0
            while True:
                i = i+1
                #try:
                #    signal.signal(signal.SIGALRM, self.read_byte()) 
                #    signal.alarm(10)
                cur_char = str(self.ser.read())

                strr = strr+ cur_char
                #except:
                #    break
                #strr = strr+ str(self.ser.read())
                print strr 
                if i > 20:
                    break
                if 'Hello' in strr:
                    break
             #   if 'STOP' not in strr:
             #       break
                
                #self.ser.flush()
            print 'msg:' + msg
            if 'Hello' in strr:
                break
            if (i > 0 and 'STOP' not in strr):
                break
            #if 'STOP' not in strr:
            #    break
            self.ser.flush()
            strr = '0'
            print msg
            print 'b'
            if msg.startswith('Hello'):
                break
            if 'Hello' in strr:
                break
            #time.sleep(3)
        self.sendMessage = ''.join(['Hello #', repr(self.pktNum)] )
        self.ser.flush()
        print "Exiting Ending_command"

    def send_msg(self, sendmsg):
        msg = self.data
        print sendmsg
        while msg == 0:
            self.xbee.tx(dest_addr='\xFF\xFF', data = sendmsg)
            self.pktNum = self.pktNum + 1
            try:
                signal.signal(signal.SIGALRM, self.receive_pkt_handler())
                signal.alarm(1)
            except:
                print self.pktNum
            msg = self.data
            print msg
            time.sleep(1)

        while(~msg.startswith('ACK')):
            self.xbee.tx(dest_addr='\xFF\xFF', data = sendmsg)
            self.pktNum = self.pktNum + 1
            msg = self.data
            time.sleep(2)
            print 'waiting_for_ack for' + sendmsg
        self.sendMessage = 'STOP_ACK'

    def read_byte(self):
        self.newest_byte = self.ser.read()
        return self.newest_byte

    def send_arrival_signal(self):
        self.sendMessage = 'ARRIVAL-'+str(self.rid)
        self.sendingCommand = True
        while(self.sendingCommand == True):
            print self.data
            print 'waiting_ack_for_arrival'
        #self.send_msg(self.sendMessage)

    def send_start_transmit_signal(self):
        self.sendMessage = 'TRANSMIT_START-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_stop_transmit_signal(self):
        self.sendMessage = 'TRANSMIT_STOP-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_set_predecessor_signal(self):
        self.sendMessage = 'SET_PREDECESSOR-'+str(self.rid)
        self.send_msg(self.sendMessage)

    def send_start_ascend_signal(self):
        self.sendMessage = 'ASCEND_START-'+str(self.rid)
        self.sendingCommand = True
        while(self.sendingCommand == True):
            print 'waiting_ack_for_ascend_start'

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

    def get_ascend_status(self):
        return self.ascend

    def set_receiver_thread(self, b):
        self.startReceive = b

    def set_transmit_thread(self, b):
        self.transmit = b

    def set_ascend(self, b):
        self.ascend = b


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

