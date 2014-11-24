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
			self.drive(-.13, .13)
			time.sleep(1)
			self.stop()
		except:
			self.stop()
		finally:
			self.stop()
	def drive_in_dist(self, dir, forwardRatio,reverseRatio):
		try:
			if (dir == True):
				self.drive(.2*forwardRatio, .2*forwardRatio)
			elif (dir == False):
				self.drive(-.2*reverseRatio, -.2*reverseRatio)
			time.sleep(3)
			self.stop()
		except:
			self.stop()
		finally:
			self.stop()
	def stop(self):
		self.drive(0, 0)


if __name__=='__main__':
	r0 = LCMBot('/01/base_cmd')
	r0.drive(.1,.1)
	time.sleep(1)
	r0.drive(0,0)
