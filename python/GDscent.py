import time

class GDscent:
    def __init__(self, zumy, xbee):
        self.r = zumy
        self.xb = xbee

        self.counter_threshold = 1
        self.counter = 0

    def drive_time_function(lastRSSI):
        return (abs(lastRSSI)-40)*0.05 + 0.2

    def stage_benefit(counter):
        return counter*0.3

    '''def measure_rssi():
        rssi, rssi_list = xb_bot.get_max_rssi()
        if rssi < -70:
            return (rssi,counter)
        print "measured rssi: ", rssi
        return rssi'''

    def calibration(self,lastRSSI,counter):
        zumy_bot = self.r
        xb_bot = self.xb

        #difference = -1
        drive_time = self.drive_time_function(lastRSSI)

        print "navigation stage ", counter

        for i in range(4):
            zumy_bot.drive_in_dist(True, 0.22,0.2,drive_time + self.stage_benefit(counter))

            rssi, rssi_list = xb_bot.get_max_rssi()
            if rssi < -70:
                return (rssi,counter)
            print "Stop point rssi: ", rssi

            difference = abs(rssi) - abs(lastRSSI) 
            if difference > 0:
                print "GETTING TO THE NEXT STOP!"
                return (rssi,0)

            time.sleep(0.1)
            zumy_bot.drive_in_dist(False,0.22,0.2, drive_time + self.stage_benefit(counter))

            lastRSSI, rssi_list = xb_bot.get_max_rssi()
            if lastRSSI < -70:
                return (lastRSSI,counter)
            print "Starting point rssi: ", lastRSSI

            zumy_bot.turn90()

        counter = counter + 1
        bestRSSI = lastRSSI
        
        # stage management
        if counter > self.counter_threshold:
            counter = 0

        return (bestRSSI,counter)

    def start(self):
    
        print "Start.... Welcome to the new age!"
        xb = self.xb

        counter = 0
        bestRSSI = 9999
        #time.sleep(20)

        while bestRSSI == 9999:
            bestRSSI, rssi_list = xb.get_max_rssi()

        print "Begin navigation and the initial starting point rssi is:  ", bestRSSI
        while bestRSSI > -70:
            bestRSSI, counter = self.calibration(bestRSSI, counter) 

        print "Victory!!!"
        self.r.stop()

        print "Exit GDscend"


        

