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
import time

def calibration(lastRSSI,xb_bot,zumy_bot,counter,f):
    difference = -1
    #drive_time = 3
    #if lastRSSI < 70:
    drive_time = (lastRSSI-40)*0.1 + 2.5 
    print "navigation stage ", counter
    data = "navigation stage" + str(counter) + "\n"
    f.write(data)
    for i in range(4):
        zumy_bot.drive_in_dist(True, 0.7,1,drive_time+counter*1)
        rssi = xb_bot.collect_max_rssi()
        print "measured rssi: ", rssi
        data = "measured rssi: " + str(rssi) + "\n"
        f.write(data)
        difference = lastRSSI - rssi
        if difference > 0:
            print "GETTING TO THE NEXT STOP!"
            f.write("GETTING TO THE NEXT STOP! \n")
            return (rssi,0)
        time.sleep(0.1)
        zumy_bot.drive_in_dist(False,1,0.7, drive_time+counter*1)
        zumy_bot.turn90()

    counter = counter + 1
    bestRSSI = lastRSSI
    if counter > 1:
        print "re-calibrating..."
        f.write("re-calibrating...\n")
        bestRSSI = xb_bot.collect_max_rssi()
        print "re-calibrated bestRSSI: ", bestRSSI
        f.write("re-calibrated bestRSSI: " + str(bestRSSI) + "\n")
        counter = 0
    return (bestRSSI,counter)

def calibration4(xb_bot,zumy_bot):
    bestRSSI = 9999;
    direction = 0;
    for i in range(4):
        zumy_bot.drive_in_dist(True,0.7,1)
        rssi = xb_bot.collect_max_rssi()
        print "initial measured rssi: %d", rssi
	if rssi < bestRSSI:
            bestRSSI = rssi
            direction = i
        zumy_bot.drive_in_dist(False,1,0.7)
        time.sleep(0.1)
        zumy_bot.turn90()

    for j in range(direction):
        zumy_bot.turn90()
    
    zumy_bot.drive_in_dist(True,0.7,1)

    return bestRSSI


if __name__ == '__main__':
        file_name = raw_input("Please input the file name: ") 
        f = open(file_name+".csv","w")
    #try:
        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        xb = XbRssi('/dev/ttyUSB0')
        #xb.start()


        counter = 0
        bestRSSI = xb.collect_max_rssi()
        while bestRSSI == 9999:
            bestRSSI = xb.collect_max_rssi()
        #bestRSSI = calibration4(xb,r)
        print "current bestRSSI: ", bestRSSI
        while bestRSSI > 38:
            bestRSSI, counter = calibration(bestRSSI, xb, r, counter,f) 
            print "current bestRSSI: ",bestRSSI
            f.write("current bestRSSI: " + str(bestRSSI) + "\n")
        print "Victory!!!"
        f.write("Victory!!!")
        r.stop()
 #except:
  #      r.stop()
   # finally:
    #    r.stop()
     #   f.close()'''
