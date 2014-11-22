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
	def turn90(self):
		try:
			self.drive(-.2, .2)
			time.sleep(1.1)
			self.drive(0, 0)
		except:
			self.drive(0, 0)
		finally:
			self.drive(0, 0)
	def drive_in_dist(self, dir):
		try:
			if (dir == True):
				self.drive(.2, .2)
			elif (dir == Flase):
				self.drive(-.2, -.2)
			time.sleep(1.2)
			self.drive(0, 0)
		except:
			self.drive(0, 0)
		finally:
			self.drive(0, 0)


if __name__=='__main__':
	r0 = LCMBot('/01/base_cmd')
	r0.drive(.1,.1)
	time.sleep(1)
	r0.drive(0,0)
