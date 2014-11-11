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
#import XBeeHelper
from xbee import XBee

ser = serial.Serial('/dev/ttyUSB0', baudrate = 57600)

xbee = XBee(ser)
#xbeeHelper = XBeeHelper.XBeeHelper("/dev/ttyUSB0")
# Continuously read and print packets
while True:
    try:
        content='transimit test \n'
            #ser.write(frame)
        
        xbee.at(frame='A', command='MY', parameter='\x20\x00')
        xbee.at(frame='B', command='CH', parameter='\x0e')
        xbee.at(frame='C', command='ID', parameter='\x99\x99')
        xbee.at(frame='D', command='CH')

        #print(xbee.wait_read_frame())
        #time.sleep(3)
        #print content
        
        pktNum = 1
        
        while(1):
            print "Sending packet #",pktNum
            message = ''.join(['Hello #', repr(pktNum)] )
            xbee.tx(dest_addr='\x20\x01', data = message)
            pktNum = pktNum + 1
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        break

xbee.halt()        
ser.close()
