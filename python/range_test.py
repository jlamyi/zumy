import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    f = open("data.csv","w")
    try:
        i = 0
        while True:
            last_RSSI = xb.get_rssi()
            last_addr = xb.get_addr()
            data = str(last_addr) + ", " + str(i) + ", -" + str(last_RSSI) + "\n"
            print "RSSI = -%d dBm @ address %d" % ( last_RSSI, last_addr )
            f.write(data)
            i = i + 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        f.close()