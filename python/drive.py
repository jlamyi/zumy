import zc_id
from Xbee import *
from LCMBot import *


if __name__=='__main__':
    rid = zc_id.get_id()
    r0 = LCMBot('{0}/base_cmd'.format(rid))
    xb = XbRssi('/dev/ttyUSB0')
    xb.start()
    while True:
        time.sleep(1)



# while(True):
#     xb.set_rssi()
#     xb.rssi()
    # r0.drive(0,0)
    # lastRSSI = xb.get_rssi()
    # print "RSSI = -%d dBm @ address %d" % ( xb.get_rssi(), xb.get_addr() )
    # print "stopped"

    # while(lastRSSI<45):
    #     xb.set_rssi()
    #     xb.rssi()
    #     r0.drive(.1,.1)
    #     lastRSSI = xb.get_rssi()
    #     print "RSSI = -%d dBm @ address %d" % ( xb.get_rssi(), xb.get_addr() )
    #     print "running"