import time, threading, serial, zc_id
from xbee import XBee
from numpy import *

class XbRssi:
    def __init__(self, serial_port): 
        self.ser = serial.Serial(serial_port, 57600)
        self.xbee = XBee(self.ser)
        self.rid = zc_id.get_id()
        self.rid = self.rid.split("/",1)[1] 
        self.xbee.at(frame='A', command='MY', parameter='\x20'+chr(int(self.rid)))
        self.xbee.at(frame='B', command='CH', parameter='\x0e')
        self.xbee.at(frame='C', command='ID', parameter='\x99\x99')
        self.updateTransmitThread = threading.Thread(target=self.transmit_loop)
        self.updateTransmitThread.daemon = True
        self.updateReceiveThread = threading.Thread(target=self.receive_loop)
        self.updateReceiveThread.daemon = True
        self.response = 0
        self.pktNum = 0
    def transmit_loop(self):
        while True:
            self.transmit_rssi()
    def receive_loop(self):
        while True:
            # self.get_max_rssi()
            self.receive_pkt()
    def transmit_rssi(self):
        # print "Sending packet #",self.pktNum
        message = ''.join(['Hello #', repr(self.pktNum)] )
        self.xbee.tx(dest_addr='\xFF\xFF', data = message)
        self.pktNum = self.pktNum + 1
        time.sleep(0.01)
    def receive_pkt(self):
        self.response = self.xbee.wait_read_frame()
        #print self.get_data() + ", RSSI = -%d dBm @ address %d" % ( self.get_rssi(), self.get_addr() )
    def get_rssi(self):
        if (self.response != 0):
            return -ord(self.response.get('rssi'))
        else:
            return 9999
    def get_addr(self):
        if (self.response != 0):
            return ord(self.response.get('source_addr')[1])
        else:
            return 0
    def get_data(self):
        if (self.response != 0):
            return self.response.get('rf_data')
        else:
            return 0
    def get_max_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_max = max(rssi_list)
        print rssi_list
        print "rssi_max = " + str(rssi_max)
        return rssi_max, rssi_list
    def get_min_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_min = min(rssi_list)
        print rssi_list
        print "rssi_min = " + str(rssi_min)
        return rssi_min, rssi_list
    def get_med_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_med = median(rssi_list)
        print rssi_list
        print "rssi_med = " + str(rssi_med)
        return rssi_med, rssi_list
    def get_avg_rssi(self):
        rssi_list = []
        for i in range(30):
            self.receive_pkt()
            rssi_list.append(self.get_rssi())
        rssi_avg = mean(rssi_list)
        print rssi_list
        print "rssi_avg = " + str(rssi_avg)
        return rssi_avg, rssi_list
    def start(self):
        self.updateTransmitThread.start()
        self.updateReceiveThread.start()
    # def close(self):
    #     self.ser.close()
    # def __del__ (self):
    #     self.ser.close()

if __name__=='__main__':
    xb = XbRssi('/dev/ttyUSB0')
    #xb.start()
    result = xb.get_max_rssi()
    print "the maximum is: ", result
    result = xb.get_min_rssi()
    print "the minimum is: ", result
    result = xb.get_avg_rssi()
    print "the average is: ", result
    result = xb.get_med_rssi()
    print "the median is: ", result


    #while True:
        # print "RSSI = -%d dBm @ address %d" % ( xb.get_max_rssi(), xb.get_addr() )
      #  time.sleep(0.5)
