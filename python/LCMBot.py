import time, lcm, fearing
from fearing import base_cmd


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


if __name__=='__main__':
    r0 = LCMBot('/01/base_cmd')
    r0.drive(.1,.1)
    time.sleep(10)
    r0.drive(0,0)
