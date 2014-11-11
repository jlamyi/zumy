
# coding: utf-8

# <img src="http://robotics.eecs.berkeley.edu/~ronf/biomimetics-thin.jpg">

## Zumy LCM Node Test

# In[17]:

import time, lcm
from fearing import base_cmd
from fearing import xbee
import zc_id
import fearing
import sys
# In[18]:

class LCMBot:
    def __init__(self, base_cmd_channel):
        self.lcm=lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        self.base_cmd_channel = base_cmd_channel
        self.msg=base_cmd()
        self.msg.header = fearing.header()
    def drive(self, l, r):
        self.msg.left_cmd=l
        self.msg.right_cmd=r
        self.lcm.publish(self.base_cmd_channel, self.msg.encode())

class XbBot:
    def __init__(self, lcm, xbee_channel):
        self.lcm=lcm
        self.lcm.subscribe(xbee_channel, self.handle_xbee)
	self.rssi = 0

    def handle_xbee(self, channel, data):
        xbee_msg = xbee.decode(data)
	self.rssi = xbee_msg.rssi;
# In[19]:

if __name__=='__main__':
    rid = zc_id.get_id()
    xb_lcm = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
    xbee_receiver_channel = '{0}/xbee'.format(rid)
    xbot = XbBot(xb_lcm, xbee_receiver_channel)
    
    robot = LCMBot('{0}/base_cmd'.format(rid))
    while True:
	xb_lcm.handle()
	time.sleep(0.1)	
	i = xbot.rssi
	print 'xbee-rssi = ' +  `i`
    	# robot.drive(0,0)
    	robot.drive(.1,.1)

def drive(l=0.,r=0.):
    robot.drive(l,r)



