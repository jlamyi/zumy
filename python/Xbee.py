
import time, threading, serial, zc_id
from xbee import XBee
from numpy import *

class XbRssi:
    # initialization
    def __init__(self, serial_port): 
        self.ser = serial.Serial(serial_port, 57600)
        self.xbee = XBee(self.ser)
        self.rid = zc_id.get_id()
        self.rid = self.rid.split("/",1)[1] 
        self.id = chr(int(self.rid))
        self.xbee.at(frame='A', command='MY', parameter='\x20'+chr(int(self.rid)))
        self.xbee.at(frame='B', command='CH', parameter='\x0e')
        self.xbee.at(frame='C', command='ID', parameter='\x99\x99')
        self.updateTransmitThread = threading.Thread(target=self.transmit_loop)
        self.updateTransmitThread.daemon = True
        self.updateReceiveThread = threading.Thread(target=self.receive_loop)
        self.updateReceiveThread.daemon = True
        self.response = 0
        self.rssi = 0
        self.addr = 0
        self.data = 0
        #self.response = self.xbee.wait_read_frame()
        #self.rssi = -ord(self.response.get('rssi'))
        #self.addr = ord(self.response.get('source_addr')[1])
        #self.data = self.response.get('rf_data')
        self.pktNum = 0
        self.sendingCommand = False
        # self.buffer = ['0']
        # self.newest_byte = '0'
        self.ser.flush()

    # define transmit and receive loop
    def transmit_loop(self):
        while True:
            self.transmit_rssi()
            time.sleep(.2)
    def receive_loop(self):
        while True:
            self.response = self.xbee.wait_read_frame()
            self.rssi = -ord(self.response.get('rssi'))
            self.addr = ord(self.response.get('source_addr')[1])
            self.data = self.response.get('rf_data')
            #print self.data + ", RSSI = %d dBm @ address %d" % ( self.rssi, self.addr )
    
    # transmitter
    def transmit_rssi(self):
        # print "Sending packet #",self.pktNum
        if (self.transmit == True):
            # message = ''.join(['Hello #', repr(self.pktNum)] )
            if (self.sendingCommand == False):
                self.sendMessage = repr(self.pktNum)
            self.xbee.tx(dest_addr='\xFF\xFF', data = self.sendMessage)
            self.pktNum = self.pktNum + 1
            time.sleep(.1)
        else:
            time.sleep(5)

    # receiver
    def get_rssi_list(self):
        rssi_list = []
        data_list = []
        rssi_list.append(self.rssi)
        data_list.append(self.data)
        i = 1
        while i<30:
           # print i
           # print self.data
            if self.data != data_list[-1]:
                rssi_list.append(self.rssi)
                data_list.append(self.data)
                i = i + 1
            time.sleep(.1)
        return rssi_list

    # data processing functions
    def get_max_rssi(self):
        rssi_list = self.get_rssi_list()
        rssi_max = max(rssi_list)
        # print rssi_list
        # print "rssi_max = " + str(rssi_max)
        return rssi_max, rssi_list
    def get_min_rssi(self):
        rssi_list = self.get_rssi_list()
        rssi_min = min(rssi_list)
        # print rssi_list
        # print "rssi_min = " + str(rssi_min)
        return rssi_min, rssi_list
    def get_med_rssi(self):
        rssi_list = self.get_rssi_list()
        rssi_med = median(rssi_list)
        # print rssi_list
        # print "rssi_med = " + str(rssi_med)
        return rssi_med, rssi_list
    def get_avg_rssi(self):
        rssi_list = self.get_rssi_list()
        rssi_avg = mean(rssi_list)
        # print rssi_list
        # print "rssi_avg = " + str(rssi_avg)
        return rssi_avg, rssi_list

    # start threading
    def start(self):
        #self.updateTransmitThread.start()
        self.updateReceiveThread.start()

    def close(self):
        self.ser.close()
    def __del__ (self):
        self.ser.close()


if __name__=='__main__':
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    # xb.receive_loop()
    # xb.get_rssi_list()
    rssi_max, rssi_list = xb.get_max_rssi()
    print "the maximum is: ", rssi_max
    rssi_min, rssi_list = xb.get_min_rssi()
    print "the minimum is: ", rssi_min
    rssi_avg, rssi_list = xb.get_avg_rssi()
    print "the average is: ", rssi_avg
    rssi_med, rssi_list = xb.get_med_rssi()
    print "the median is: ", rssi_med
