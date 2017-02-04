import time
import threading

myDelay = 0

def move_delay(sec, state):
	global myDelay
	def func_wrapper():
		if state:
			print("On")
			move_delay(sec, False)
		else:
			print("Off")
			move_delay(sec, True)
        
	myDelay = threading.Timer(sec, func_wrapper)
	myDelay.start()
	return myDelay

def cancel_delay():
	print("cancel")
	myDelay.cancel()