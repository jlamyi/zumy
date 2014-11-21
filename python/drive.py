import time, lcm
from fearing import base_cmd
import fearing
import zc_id
import serial
from xbee import XBee
import sys

class LCMBot:
    def __init__(self, base_cmd_channel):
        self.lcm=lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        self.base_cmd_channel = base_cmd_channel
        self.msg=base_cmd()
        self.msg.header = fearing.header()
    def drive(self, l, r):
        self.msg.left_cmd=l
        self.msg.right_cmd=r
        self.lcm.publish(self.base_cmd_channel, self.msg.encode())

class XbRssi:

    def __init__(self, serial_port): 
        self.ser = serial.Serial(serial_port, 57600)
        self.xbee = XBee(self.ser)
        self.rid = zc_id.get_id()
        self.rid = self.rid.split("/",1)[1] 
        self.xbee.at(frame='A', command='MY', parameter='\x20'+chr(int(self.rid)))
        self.xbee.at(frame='B', command='CH', parameter='\x0e')
        self.xbee.at(frame='C', command='ID', parameter='\x99\x99')
        # self.xbee.at(frame='D', command='CH')
        self.response = 0
        self.pktNum = 0

    def set_rssi(self):
        print "Sending packet #",self.pktNum
        message = ''.join(['Hello #', repr(self.pktNum)] )
        self.xbee.tx(dest_addr='\xFF\xFF', data = message)
        self.pktNum = self.pktNum + 1
        time.sleep(0.5)

    def rssi(self):
        self.response = self.xbee.wait_read_frame()
        #time.sleep(1)
        print "RSSI = -%d dBm @ address %d" % ( ord(self.response.get('rssi')), ord(self.response.get('source_addr')[1]) )

    def get_rssi(self):
        return ord(self.response.get('rssi'))
    def get_addr(self):
        return ord(self.response.get('source_addr')[1])
    def close(self):
        self.ser.close()
    def __del__ (self):
        self.ser.close()







rid = zc_id.get_id()
r0 = LCMBot('{0}/base_cmd'.format(rid))
xb = XbRssi('/dev/ttyUSB0')
while(True):
    xb.set_rssi()
    xb.rssi()
    r0.drive(0,0)
    lastRSSI = xb.get_rssi()
    print "stopped"

    while(lastRSSI<45):
        xb.set_rssi()
        xb.rssi()
        r0.drive(.1,.1)
        lastRSSI = xb.get_rssi()
        print "running"


# robot.drive(.1,.1)
# time.sleep(10)
# robot.drive(0,0)
