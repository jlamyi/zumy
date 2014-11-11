from xbee import XBee
import serial, time

def main():
    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    ser = serial.Serial('/dev/ttyUSB0', 57600)
    xbee = XBee(ser)
    xbee.at(frame='A', command='MY', parameter='\x20\x01')
    xbee.at(frame='B', command='CH', parameter='\x0e')
    xbee.at(frame='C', command='ID', parameter='\x99\x99')
    
    try:
    
        while(1):
    #       xbee.send('at', frame_id='A', command='DB')
            response = xbee.wait_read_frame()
            print response
            lastRSSI = response.get('rssi')
            print "RSSI = -%d dBm" % ord(lastRSSI)
            
        
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    
if __name__ == '__main__':
    main()
