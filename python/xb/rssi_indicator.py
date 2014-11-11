#!/usr/bin/env python
"""
shell.py

Amit Snyderman, 2009
<amit@amitsnyderman.com>

Updated by Paul Malmsten, 2010
pmalmsten@gmail.com

Provides a simple shell for testing XBee devices. Currently, the shell
only allows one to parse and print received data; sending is not
supported.
"""
# $Id: xbee-serial-terminal.py 7 2009-12-30 16:25:08Z amitsnyderman $

import sys, time, cmd, serial, binascii,time
from xbee import XBee

ser = serial.Serial('/dev/ttyUSB1', 9600)

xbee = XBee(ser)
'''
time.sleep(2)
ser.write('+++')
time.sleep(2)'''
# Continuously read and print packets
while True:
    try:
        #xbee.at(command='DB')
        read = xbee.wait_read_frame()
        print read
    except KeyboardInterrupt:
        break
        
ser.close()
