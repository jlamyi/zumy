import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    f = open("data.csv","w")
    i = 0
    while True:
        lastRSSI = xb.get_rssi()
        data = str(i) + ", -" + str(lastRSSI) +"\n"
        print "RSSI = -%d dBm @ address %d" % ( xb.get_rssi(), xb.get_addr() )
        f.write(data)
        i = i + 1
        time.sleep(0.5)
