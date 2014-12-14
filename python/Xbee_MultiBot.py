import time, threading, serial
from numpy import *
from Xbee import XbRssi

class Xbee_MultiBot(XbRssi):
    def __init__(self,serial_port): 
        XbRssi.__init__(self,serial_port)  
        '''      
        self.predecessor = 0
        self.successor = 0
        self.transmit = True
        self.ascend = False
        self.descend = False
        self.startReceive = True
        self.sendMessage = self.id+'PKT'
        self.cmdList = []
        '''

    # receiver
    def get_rssi_list(self, bot_id):
        rssi_list = []
        data_list = []
        rssi_list.append(self.rssi)
        data_list.append(self.data)
        i = 1
        while i<30:
           # print i
           # print self.data
            if self.data != data_list[-1] and bot_id == ???:
                rssi_list.append(self.rssi)
                data_list.append(self.data)
                i = i + 1
            time.sleep(.1)
        return rssi_list

    # data processing functions
    '''def get_max_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_max = max(rssi_list)
        # print rssi_list
        # print "rssi_max = " + str(rssi_max)
        return rssi_max, rssi_list
    def get_min_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_min = min(rssi_list)
        # print rssi_list
        # print "rssi_min = " + str(rssi_min)
        return rssi_min, rssi_list
    def get_med_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_med = median(rssi_list)
        # print rssi_list
        # print "rssi_med = " + str(rssi_med)
        return rssi_med, rssi_list
    def get_avg_rssi(self,bot_id):
        rssi_list = self.get_rssi_list(bot_id)
        rssi_avg = mean(rssi_list)
        # print rssi_list
        # print "rssi_avg = " + str(rssi_avg)
        return rssi_avg, rssi_list

    def get_sender_id(self, msg):
        start_index = msg.index('-')
        return msg[start_index+1:]'''
   
'''
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
'''
