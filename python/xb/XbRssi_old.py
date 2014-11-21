from xbee import XBee
import sys
import serial, time, threading
import zc_id

class XbRssi:
   def __init__(self, serial_port): 
   	ser = serial.Serial(serial_port, 57600)
    	self.xbee = XBee(ser)
        rid = zc_id.get_id()
        rid = rid.split("/",1)[1] 
    	self.xbee.at(frame='A', command='MY', parameter='\x20'+chr(int(rid)))
    	self.xbee.at(frame='B', command='CH', parameter='\x0e')
    	self.xbee.at(frame='C', command='ID', parameter='\x99\x99')

	self.updateThread = threading.Thread(target=self._rssi_loop)
	self.updateThread.daemon = True
	self.lastRSSI = 0
        self.lastAddr = 0

   def _rssi_loop(self):

	pktNum = 1
        
        while True:

            print "Sending packet #",pktNum
            message = ''.join(['Hello #', repr(pktNum)] )
            self.xbee.tx(dest_addr='\xFF\xFF', data = message)
            pktNum = pktNum + 1
            time.sleep(0.5)
 
            response = self.xbee.wait_read_frame()
            self.lastRSSI = ord(response.get('rssi'))
            self.lastAddr = ord(response.get('source_addr')[1])

            print "RSSI = -%d dBm @ address %d" % (self.lastRSSI,self.lastAddr)
	    time.sleep(1)
	
   def getRssi(self):
	return self.lastRSSI

   def getAddr(self):
	return self.lastAddr
 
   def start(self):
	self.updateThread.start()
    
if __name__=='__main__':
   xb = XbRssi('/dev/ttyUSB0')
   xb.start()	
   time.sleep(100)

