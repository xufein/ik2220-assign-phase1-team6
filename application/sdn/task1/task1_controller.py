from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
from task1_firewall6 import task1_FireWall6
from task1_firewall7 import task1_FireWall7

def launch ():
	controller = task_1_controller()
	core.register("controller", controller)

class task_1_controller (object):
	def __init__ (self):
		core.openflow.addListeners(self)

	def _handle_ConnectionUp (self, event):
		dpid = event.dpid

		if dpid == 1 or dpid == 2 or dpid == 3 or dpid == 4 or dpid == 5 or dpid == 8 or dpid == 9 or dpid == 10 or dpid == 11:
			LearningSwitch(event.connection, False)

		elif dpid == 6:
			task1_FireWall6(event.connection)

		elif dpid == 7:
			task1_FireWall7(event.connection)
			



