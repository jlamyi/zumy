import zc_id
from Xbee import *
from LCMBot import *
from GAscent import *

if __name__ == '__main__':
        #file_name = raw_input("Please input the file name: ") 
        #f = open(file_name+".csv","w")

        rid = zc_id.get_id()
        r = LCMBot('{0}/base_cmd'.format(rid))
        xb = XbRssi('/dev/ttyUSB0')
        xb.start()

        ascending_bot = GAscent(r, xb)
       #s xb.set_transmit_thread(False)

        while True:
            ascend = xb.get_ascend_status()

            if ascend == True:
                ascending_bot.start()
                xb.set_ascend(False)
     #           xb.set_receiver_thread(False)
            bestRSSI,rssi_list = xb.get_max_rssi()
            print xb.sendMessage
            time.sleep(3)
        	#else:
        #		sentry_bot.start()
       
