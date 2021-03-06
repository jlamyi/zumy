
# coding: utf-8

# <img src="http://robotics.eecs.berkeley.edu/~ronf/biomimetics-thin.jpg">

## Robot Test

# In[1]:

import time
from python.mbedrpc import *
import threading

from xbee import XBee
import serial, time
# In[2]:

class Motor:
    def __init__(self, a1, a2):
        self.a1=a1
        self.a2=a2
    def cmd(self, speed):
        if speed >=0:
            self.a1.write(speed)
            self.a2.write(0)
        else:
            self.a1.write(0)
            self.a2.write(-speed)
class Robot:
    def __init__(self, dev='/dev/ttyACM0'):
        self.mbed=SerialRPC(dev, 115200)
        a1=PwmOut(self.mbed, p21)
        a2=PwmOut(self.mbed, p22)
        b1=PwmOut(self.mbed, p23)
        b2=PwmOut(self.mbed, p24)
        self.m_right = Motor(a1, a2)
        self.m_left = Motor(b1, b2)
        self.enabled=True
        self.last_left=0
        self.last_right=0
        self.sensors=[]
        for i in (p20,p19,p18,p17,p16,p15):
            self.sensors.append(AnalogIn(self.mbed, i))
        self.rlock=threading.Lock()
    def enable(self):
        self.rlock.acquire()
        self.enabled=True
        self._cmd(self.last_left, self.last_right)
        self.rlock.release()
    def disable(self):
        self.rlock.acquire()
        self.enabled=False
        self._cmd(self.last_left, self.last_right)
        self.rlock.release()
    def drive(self, left, right):
        self.rlock.acquire()
        self._cmd(left, right)
        self.rlock.release()
    def cmd(self, left, right):
        self.rlock.acquire()
        self._cmd(left, right)
        self.rlock.release()
    def _cmd(self, left, right):
        self.last_left=left
        self.last_right=right
        if self.enabled:
            self.m_left.cmd(-left)
            self.m_right.cmd(right)
        else:
            self.m_left.cmd(0)
            self.m_right.cmd(0)
    def read_sensors(self):
        """ returns an array of the line sensor reflectance values
        """
        self.rlock.acquire()
        def read(sensor): return sensor.read()
        retu=map(read, self.sensors)
        self.rlock.release()
        return retud


# In[4]:

#ls /dev/ttyACM*


# In[5]:

r0=Robot('/dev/ttyACM0')

# xbee setup

ser = serial.Serial('/dev/ttyUSB0', 57600)
xbee = XBee(ser)
xbee.at(frame='A', command='MY', parameter='\x20\x01')
xbee.at(frame='B', command='CH', parameter='\x0e')
xbee.at(frame='C', command='ID', parameter='\x99\x99')


try:
	print "start turning, wait.."
	r0.cmd(-.1,.1)
	time.sleep(1)
	print "stop turning"
	r0.cmd(0, 0)
	
except:
	r0.cmd(0, 0)
	print "error"
finally:
	r0.cmd(0, 0)

# In[6]:
#while(True):
#    #print "in the loop"
#    response = xbee.wait_read_frame()
#    print response
#    r0.cmd(0,0)
#    lastRSSI = response.get('rssi')
#    while(ord(lastRSSI)<45):
#        r0.cmd(.3,.3)
#        response = xbee.wait_read_frame()
#            #print response
#        lastRSSI = response.get('rssi')
#        print "RSSI = -%d dBm" % ord(lastRSSI)
	


# In[7]:

#r0.cmd(0,0)


# Now, Restart the kernel to release ownership of the serial device:
# 
# File > Kernel > Restart
