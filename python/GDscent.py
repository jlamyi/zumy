import time

class GDscent:
    def __init__(self, zumy, xbee):
        self.r = zumy
        self.xb = xbee

        self.counter_threshold = 1
        self.counter = 0
        self.stop_rssi = -60

        self.lastRSSI = 9999
        self.newRSSI = 0
        self.startRSSI = 0
        self.endRSSI = 0

    def drive_time_function(self,lastRSSI):
        return (abs(lastRSSI)-40)*0.05 + 0.2

    def stage_benefit(self):
        return self.counter*0.3

    def measure_rssi(self,msg):
        self.newRSSI, rssi_list = self.xb.get_max_rssi()
        print str(msg) + ": ", self.newRSSI

    def check_end(self):
        if self.newRSSI < self.stop_rssi:
            self.lastRSSI = self.newRSSI
            return True
        return False 

    def calibration(self):
        zumy_bot = self.r
        xb_bot = self.xb

        drive_time = self.drive_time_function(self.lastRSSI)

        print "++++++++++++++++++++++++++++++++++"
        print "navigation stage ", self.counter

        for i in range(4):

            print "-----------------------------"
            self.measure_rssi("Starting point rssi")
            if self.check_end():
                return
            self.startRSSI = self.newRSSI


            zumy_bot.drive_in_dist(True, 0.22,0.2,drive_time + self.stage_benefit())

            self.measure_rssi("Stop point rssi")
            if self.check_end():
                return
            self.endRSSI = self.newRSSI

            difference = abs(self.endRSSI) - abs(self.startRSSI) 
            if difference > 0:
                print "GETTING TO THE NEXT STOP!"
                self.counter = 0
                self.lastRSSI = self.endRSSI
                return 

            time.sleep(0.1)
            zumy_bot.drive_in_dist(False,0.22,0.2, drive_time + self.stage_benefit())
            zumy_bot.turn90()

        # stage management   
        self.counter = self.counter + 1
        if self.counter > self.counter_threshold:
            self.counter = 0

        return 

    def start(self):
    
        print "Start.... Welcome to the new age!"
        xb = self.xb

        #time.sleep(20)

        while self.lastRSSI == 9999:
            self.lastRSSI, rssi_list = xb.get_max_rssi()
            print "waiting for signal"

        while self.lastRSSI > self.stop_rssi:
            self.calibration()

        print "Victory!!!"
        self.r.stop()

        print "Exit GDscend"


        

