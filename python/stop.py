
# coding: utf-8

# <img src="http://robotics.eecs.berkeley.edu/~ronf/biomimetics-thin.jpg">

## Zumy LCM Node Test

# In[17]:

import time, lcm
from fearing import base_cmd
import fearing
import zc_id

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


# In[19]:

if __name__=='__main__':
    rid = zc_id.get_id()
    robot = LCMBot(s'{0}/base_cmd'.format(rid))
    robot.drive(0,0)
    robot.drive(.1,.1)
    robot.drive(0,0)

def drive(l=0.,r=0.):
    robot.drive(l,r)



