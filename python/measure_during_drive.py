import zc_id
from Xbee import *
from LCMBot import *

import time

if __name__=='__main__':
    rid = zc_id.get_id()
    r = LCMBot('{0}/base_cmd'.format(rid))
    
    file_name = raw_input("Please input the file name: ")
    f = open(file_name + ".csv", "w")

    xb = XbRssi('/dev/ttyUSB0')

    start_time = time.time()
    driving_time = 5
    i = 0

    r.drive(0.18,0.18)
   
    while time.time()-start_time < driving_time: 
        rssi, rssi_list = xb.get_max_rssi()
        f.write("Position #" + str(i) + "rssi = " + str(rssi) + " " + str(rssi_list) + "\n")
        i = i + 1

    r.stop()
    f.close()    

