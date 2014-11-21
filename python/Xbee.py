import time
# import lcm
import threading
# from fearing import base_cmd
# import fearing
import serial
from xbee import XBee
# import sys

class XbRssi:
    def __init__(self, serial_port): 
        self.ser = serial.Serial(serial_port, 57600)
        self.xbee = XBee(self.ser)
        self.rid = '/01'
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
            self.receive_rssi()
    def transmit_rssi(self):
        print "Sending packet #",self.pktNum
        message = ''.join(['Hello #', repr(self.pktNum)] )
        self.xbee.tx(dest_addr='\xFF\xFF', data = message)
        self.pktNum = self.pktNum + 1
        time.sleep(0.5)
    def receive_rssi(self):
        self.response = self.xbee.wait_read_frame()
        print "RSSI = -%d dBm @ address %d" % ( self.get_rssi(), self.get_addr() )
    def get_rssi(self):
        return ord(self.response.get('rssi'))
    def get_addr(self):
        return ord(self.response.get('source_addr')[1])
    def start(self):
        self.updateTransmitThread.start()
        self.updateReceiveThread.start()
    # def close(self):
    #     self.ser.close()
    # def __del__ (self):
    #     self.ser.close()

if __name__=='__main__':
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    time.sleep(10)