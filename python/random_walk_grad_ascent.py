
# coding: utf-8

# <img src="http://robotics.eecs.berkeley.edu/~ronf/biomimetics-thin.jpg">

## Robot Test


# import time
# from mbedrpc import *
# import threading
# import signal
# from xbee import XBee
# import serial, time

# class Motor:
#     def __init__(self, a1, a2):
#         self.a1=a1
#         self.a2=a2
#     def cmd(self, speed):
#         if speed >=0:
#             self.a1.write(speed)
#             self.a2.write(0)
#         else:
#             self.a1.write(0)
#             self.a2.write(-speed)
# class Robot:
#     def __init__(self, dev='/dev/ttyACM0'):
#         self.mbed=SerialRPC(dev, 115200)
#         a1=PwmOut(self.mbed, p21)
#         a2=PwmOut(self.mbed, p22)
#         b1=PwmOut(self.mbed, p23)
#         b2=PwmOut(self.mbed, p24)
#         self.m_right = Motor(a1, a2)
#         self.m_left = Motor(b1, b2)
#         self.enabled=True
#         self.last_left=0
#         self.last_right=0
#         self.sensors=[]
#         for i in (p20,p19,p18,p17,p16,p15):
#             self.sensors.append(AnalogIn(self.mbed, i))
#         self.rlock=threading.Lock()
#     def enable(self):
#         self.rlock.acquire()
#         self.enabled=True
#         self._cmd(self.last_left, self.last_right)
#         self.rlock.release()
#     def disable(self):
#         self.rlock.acquire()
#         self.enabled=False
#         self._cmd(self.last_left, self.last_right)
#         self.rlock.release()
#     def drive(self, left, right):
#         self.rlock.acquire()
#         self._cmd(left, right)
#         self.rlock.release()
#     def cmd(self, left, right):
#         self.rlock.acquire()
#         self._cmd(left, right)
#         self.rlock.release()
#     def _cmd(self, left, right):
#         self.last_left=left
#         self.last_right=right
#         if self.enabled:
#             self.m_left.cmd(-left)
#             self.m_right.cmd(right)
#         else:
#             self.m_left.cmd(0)
#             self.m_right.cmd(0)
#     def read_sensors(self):
#         """ returns an array of the line sensor reflectance values
#         """
#         self.rlock.acquire()
#         def read(sensor): return sensor.read()
#         retu=map(read, self.sensors)
#         self.rlock.release()
#         return retud
#     def close(self):
#         self.mbed.ser.close()

#     def __del__ (self):
#         self.cmd(0,0)
#         self.mbed.ser.close()






# the functions need to be added to Class Robot
# 1. def drive_in_dist(self, bool dir) (drive certain distance) (speed and time is default) (true is forward, false is backword)
#    inputs:
#    	(dir: direction, forward or backward)
# 2. def turn90(self) (turn certain angle) (speed and time is default)
#
# external functions
# 1. def calibration(int lastRSSI, Robot r) (find the right angle to go) (true is forward, false is backword)
#    input:
#       (lastRSSI: the best rssi value from the last location)
#	(r: the robot that is in use)
#    output:
#    	(return a bool value, the robot should go forward or backward)
#	(return the best rssi value at the current location)
# 2. def collect_rssi() (collect 30 rssi in the same place, and return the current rssi) 
#    output: the estimated rssi value according to the 30 samples (should be an integer!!!!)

import zc_id
from Xbee import *
from LCMBot import *


def calibration(lastRSSI,xb_bot,zumy_bot):
    bestDir = 0
    for i in range(4):
        rssi = xb_bot.collect_max_rssi()
        if i==0:
            if rssi > lastRSSI:
                return (False, lastRSSI) 
            bestRSSI = rssi
        if rssi < bestRSSI:
            bestRSSI = rssi
            bestDir = i;
        zumy_bot.turn90()
 
    for j in range(bestDir):
        zumy_bot.turn90()     
        
    return (True, bestRSSI)


rid = zc_id.get_id()
r0 = LCMBot('{0}/base_cmd'.format(rid))
xb = XbRssi('/dev/ttyUSB0')
xb.start()
# r0.turn90()
RSSI = xb.get_rssi()
time.sleep(1)
RSSI = xb.get_rssi()
print RSSI
while(RSSI>38):
    r0.turn90()
    direction, bestRSSI = calibration(xb.get_rssi(), xb, r0)
    if bestRSSI < 38:
       break 
    r0.drive_in_dist(direction)