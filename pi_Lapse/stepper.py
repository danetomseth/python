import RPi.GPIO as GPIO ## Import GPIO library
import time
import threading




#Stepper vars
slide_dir_pin = 23
slide_step_pin = 24
slide_enable = 25

pan_dir_pin = 4
pan_step_pin = 17
pan_enable = 18


tilt_dir_pin = 5
tilt_step_pin = 6
tilt_enable = 12


slide_limit_left = 20
slide_limit_right = 21

pan_limit = 27
tilt_limit = 22


stop_button = 13

joystick_down = 16
joystick_up = 19
joystick_right = 26
joystick_left = 20

# 16 , 19 , 26



#Step mode pins
# M0 = 22
# M1 = 27
# M2 = 17

output_List = [slide_dir_pin, slide_step_pin, pan_dir_pin, pan_step_pin, tilt_dir_pin, tilt_step_pin, slide_enable, pan_enable, tilt_enable]
# output_List = [slide_dir_pin, slide_step_pin, slide_enable]

# Constants
LEFT = False
RIGHT = True

HOME = False
AWAY = True

UP = False
DOWN = True


TILT_OFFSET = 4100
PAN_OFFSET = 1000
SLIDE_OFFSET = 4000

SLOW = 0.002
MEDIUM = 0.0001
FAST = 0.0002
TURBO = 0.0001

FULL_PAN_STEP_DEGREE = 62.69 #number of steps/degree for pan

FULL_SLIDE_STEP_MM = 13.4983  #number of steps/mm for slider

FULL_TILT_STEP_DEGREE = 1.0

PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE * 4.0
SLIDE_STEP_MM = FULL_SLIDE_STEP_MM * 4.0
TILT_STEP_DEGREE = FULL_TILT_STEP_DEGREE * 8.0

step_mode_label = "1/4 STEPS"

#### ---- user variables ---- ####

test_slide_amount = 0
test_pan_amount = 0
test_tilt_amount = 0

programed_tilt_steps = 0
tilt_step_ratio = 1.0


test_pan_num = 2
test_tilt_num = 2

#-----PAN
set_pan_degrees = 20
set_pan_direction = LEFT
set_pan_speed = MEDIUM
pan_steps_cycle = 5
pan_step_ratio = 1.0


programed_pan_steps = 0

pan_home_set = False
pan_home_degree_max = 30
pan_start_set = False

quick_pan_speed = 0.0005

pan_active = True


#-----SLIDE
set_slide_distance = 200
set_slide_direction = HOME
set_slide_speed = FAST
slide_steps_cycle = 25
slide_step_ratio = 1.0

programed_slide_steps = 0

activeStepping = False
slide_speed = 0.01

quick_slide_speed = 0.0005

slide_active = True


#-----TILT

set_tilt_direction = UP
set_tilt_speed = SLOW
set_tilt_degrees = 10
tilt_degree_mac = 30

tilt_active = True
tilt_steps_cycle = 10

quick_tilt_speed = 0.0005

#-----Program
total_program_steps = 1200
slide_to_pan_ratio = 5
program_cycle_count = 0



slide_direction = LEFT
pan_direction = LEFT

# step_size = 100



def gpio_setup():
	# GPIO.setmode(GPIO.BCM) ## Use board pin numbering
	GPIO.setmode(GPIO.BCM) ## Use board pin numbering

	# GPIO.setup(slide_limit_left, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(slide_limit_right, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(joystick_down, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(joystick_up, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(joystick_right, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(joystick_left, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(tilt_limit, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(pan_limit, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	for x in output_List:
		GPIO.setup(x, GPIO.OUT) ##setup gpio as out
		GPIO.output(x, False) ##set initial state to low

	# change_step_mode(0.25)


def calculate_steps_cycle(pictures):
	global tilt_steps_cycle
	global pan_steps_cycle
	global slide_steps_cycle
	tilt_steps_cycle = int(round(programed_tilt_steps / pictures))
	pan_steps_cycle = int(round(programed_pan_steps / pictures))
	slide_steps_cycle = int(round(programed_slide_steps / pictures))
	print("TILT: " + str(tilt_steps_cycle))
	print("PAN: " + str(pan_steps_cycle))
	print("SLIDE: " + str(slide_steps_cycle))

def calculate_ratios():
	global tilt_step_ratio
	global pan_step_ratio
	global slide_step_ratio

	# tilt_step_ratio = round(float(programed_slide_steps) / float(programed_tilt_steps), 3)
	# pan_step_ratio = round(float(programed_slide_steps) / float(programed_pan_steps), 3)
	if programed_tilt_steps > 0:
		tilt_step_ratio = int(round(float(programed_slide_steps) / float(programed_tilt_steps)))
	else:
		tilt_step_ratio = 0
	if programed_pan_steps > 0:
		pan_step_ratio = int(round(float(programed_slide_steps) / float(programed_pan_steps)))
	else:
		pan_step_ratio = 0

	print("Tilt: " + str(tilt_step_ratio))
	print("Pan: " + str(pan_step_ratio))

def preview_timelapse_fluid():
	steps_taken = 0
	tilt_steps = 0
	pan_steps = 0
	enable_pan()
	enable_tilt()
	enable_slide()

	while steps_taken < programed_slide_steps:
		if stop():
			break
		GPIO.output(slide_step_pin, True)
		
		if tilt_step_ratio > 0:
			if steps_taken % tilt_step_ratio == 0:
				GPIO.output(tilt_step_pin, True)
				tilt_steps += 1
		
		if pan_step_ratio > 0:
			if steps_taken % pan_step_ratio == 0:
				GPIO.output(pan_step_pin, True)
				pan_steps += 1
		
		time.sleep(MEDIUM)
		GPIO.output(tilt_step_pin, False)
		GPIO.output(pan_step_pin, False)
		GPIO.output(slide_step_pin, False)
		time.sleep(MEDIUM)
		steps_taken += 1

	disable_tilt()
	disable_pan()
	disable_slide()
	print("Actual tilt: " + str(tilt_steps))
	print("Actual pan: " + str(pan_steps))


def preview_timelapse():
	count = 0
	steps_taken = 0
	enable_pan()
	enable_tilt()
	enable_slide()

	while 1:
		if stop():
			break
		if steps_taken < programed_tilt_steps:
			GPIO.output(tilt_step_pin, True)
		
		if steps_taken < programed_pan_steps:
			GPIO.output(pan_step_pin, True)
		
		if steps_taken < programed_slide_steps:
			GPIO.output(slide_step_pin, True)



		time.sleep(MEDIUM)
		GPIO.output(tilt_step_pin, False)
		GPIO.output(pan_step_pin, False)
		GPIO.output(slide_step_pin, False)
		if steps_taken > programed_tilt_steps and steps_taken > programed_slide_steps and steps_taken > programed_pan_steps:
			print("END")
			break
		time.sleep(MEDIUM)
		steps_taken += 1

	disable_tilt()
	disable_pan()
	disable_slide()

def reset_timelapse_start():
	count = 0
	steps_taken = 0
	panOpp = not set_pan_direction
	tiltOpp = not set_tilt_direction
	slideOpp = not set_slide_direction

	GPIO.output(pan_dir_pin, panOpp)
	GPIO.output(tilt_dir_pin, tiltOpp)
	GPIO.output(slide_dir_pin, slideOpp)


	enable_pan()
	enable_tilt()
	enable_slide()

	while 1:
		if stop():
			break
		if steps_taken < programed_tilt_steps:
			GPIO.output(tilt_step_pin, True)
		
		if steps_taken < programed_pan_steps:
			GPIO.output(pan_step_pin, True)
		
		if steps_taken < programed_slide_steps:
			GPIO.output(slide_step_pin, True)



		time.sleep(MEDIUM)
		GPIO.output(tilt_step_pin, False)
		GPIO.output(pan_step_pin, False)
		GPIO.output(slide_step_pin, False)
		if steps_taken > programed_tilt_steps and steps_taken > programed_slide_steps and steps_taken > programed_pan_steps:
			print("END")
			break
		time.sleep(MEDIUM)
		steps_taken += 1
		
	disable_tilt()
	disable_pan()
	disable_slide()
	GPIO.output(pan_dir_pin, set_pan_direction)
	GPIO.output(tilt_dir_pin, set_tilt_direction)
	GPIO.output(slide_dir_pin, set_slide_direction)




def timelapse_step():
	enable_tilt()
	for x in range(tilt_steps_cycle):
		if stop():
			return True
		GPIO.output(tilt_step_pin, True)
		time.sleep(set_tilt_speed)
		GPIO.output(tilt_step_pin, False)
		time.sleep(set_tilt_speed)
	disable_tilt()

	enable_pan()
	for x in range(pan_steps_cycle):
		if stop():
			return True
		GPIO.output(pan_step_pin, True)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, False)
		time.sleep(set_pan_speed)
	disable_pan()	

	enable_slide()
	for x in range(slide_steps_cycle):
		if stop():
			return True
		GPIO.output(slide_step_pin, True)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, False)
		time.sleep(set_slide_speed)
	disable_slide()	
	return False	


def timelapse_slide_end():
	global programed_slide_steps
	programed_slide_steps = 0
	GPIO.output(slide_dir_pin, set_slide_direction)
	enable_slide()
	while stop() == False:
		programed_slide_steps += 1
		GPIO.output(slide_step_pin, True)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, False)
		time.sleep(set_slide_speed)

	disable_slide()


def timelapse_pan_end():
	global programed_pan_steps
	programed_pan_steps = 0
	GPIO.output(pan_dir_pin, set_pan_direction)
	enable_pan()
	while stop() == False:
		programed_pan_steps += 1
		GPIO.output(pan_step_pin, True)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, False)
		time.sleep(set_pan_speed)

	disable_pan()

def timelapse_tilt_end():
	global programed_tilt_steps
	programed_tilt_steps = 0
	GPIO.output(tilt_dir_pin, set_tilt_direction)
	enable_tilt()
	while stop() == False:
		programed_tilt_steps += 1
		GPIO.output(tilt_step_pin, True)
		time.sleep(set_tilt_speed)
		GPIO.output(tilt_step_pin, False)
		time.sleep(set_tilt_speed)

	disable_tilt()

def timelapse_reset_start():
	pan_opp = not set_pan_direction
	tilt_opp = not set_tilt_direction
	slide_opp = not set_slide_direction

def test_enable():
	print("enable")
	GPIO.output(slide_enable, True)


	

def test_disable():
	print("disable")
	GPIO.output(slide_enable, False)

def test_start():
	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	stepCount = 0
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00015)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00015)
		stepCount += 1
	GPIO.output(slide_enable, False)
	print("SLIDE Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	GPIO.output(pan_enable, True)
	GPIO.output(pan_dir_pin, RIGHT)
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(pan_enable, False)
	print("PAN Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	GPIO.output(tilt_enable, True)
	GPIO.output(tilt_dir_pin, DOWN)
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(tilt_enable, False)
	print("TILT Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0

def test_end():
	global test_slide_amount
	global test_pan_amount
	global test_pan_num
	global test_tilt_amount
	global test_tilt_num

	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, AWAY)
	stepCount = 0
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00015)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00015)
		stepCount += 1
	GPIO.output(slide_enable, False)
	time.sleep(1)
	test_slide_amount = stepCount
	stepCount = 0
	GPIO.output(pan_enable, True)
	GPIO.output(pan_dir_pin, LEFT)
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(pan_enable, False)
	test_pan_amount = stepCount
	time.sleep(1)
	stepCount = 0
	GPIO.output(tilt_enable, True)
	GPIO.output(tilt_dir_pin, UP)
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(tilt_enable, False)
	test_tilt_amount = stepCount
	time.sleep(1)


	print("Counts: ")
	print("Slide: " + str(test_slide_amount))
	print("Pan: " + str(test_pan_amount))
	print("Tilt: " + str(test_tilt_amount))
	test_tilt_num = int(round(test_slide_amount / test_tilt_amount))
	test_tilt_num = int(round(test_slide_amount / test_pan_amount))
	print("Tilt num: " + str(test_tilt_num))
	print("Pan num: " + str(test_pan_num))


def test_run():
	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	for x in range(test_slide_amount):
		if stop == True:
			print("EXIT")
			break
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00015)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00015)
	GPIO.output(slide_enable, False)
	time.sleep(1)
	GPIO.output(pan_enable, True)
	GPIO.output(pan_dir_pin, RIGHT)
	for x in range(test_pan_amount):
		if stop == True:
			print("EXIT")
			break
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
	GPIO.output(pan_enable, False)
	time.sleep(1)
	GPIO.output(tilt_enable, True)
	GPIO.output(tilt_dir_pin, DOWN)
	for x in range(test_tilt_amount):
		if stop == True:
			print("EXIT")
			break
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
	GPIO.output(tilt_enable, False)
	time.sleep(1)



def test_video_run():
	moveSteps = test_slide_amount
	GPIO.output(slide_enable, True)
	GPIO.output(pan_enable, True)
	GPIO.output(tilt_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	GPIO.output(pan_dir_pin, RIGHT)
	GPIO.output(tilt_dir_pin, UP)
	for x in range(moveSteps):
		if stop() == True:
			print("limit break")
			break
		if x % test_tilt_num == 0:
			GPIO.output(slide_step_pin, True)
			GPIO.output(pan_step_pin, True)
			GPIO.output(tilt_step_pin, True)
			time.sleep(0.0005)
			GPIO.output(slide_step_pin, False)
			GPIO.output(pan_step_pin, False)
			GPIO.output(tilt_step_pin, False)
		elif x % test_pan_num == 0:
			GPIO.output(slide_step_pin, True)
			GPIO.output(pan_step_pin, True)
			time.sleep(0.0005)
			GPIO.output(slide_step_pin, False)
			GPIO.output(pan_step_pin, False)
		else:
			GPIO.output(slide_step_pin, True)
			time.sleep(0.0005)
			GPIO.output(slide_step_pin, False)
		time.sleep(0.0005)

	GPIO.output(slide_enable, False)
	GPIO.output(pan_enable, False)
	GPIO.output(tilt_enable, False)



def move_all():
	moveSteps = 22000
	GPIO.output(slide_enable, True)
	GPIO.output(pan_enable, True)
	GPIO.output(tilt_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	GPIO.output(pan_dir_pin, RIGHT)
	GPIO.output(tilt_dir_pin, UP)
	for x in range(moveSteps):
		if stop() == True:
			print("limit break")
			break
		if x % 4 == 0:
			GPIO.output(slide_step_pin, True)
			GPIO.output(pan_step_pin, True)
			GPIO.output(tilt_step_pin, True)
			time.sleep(0.0005)
			GPIO.output(slide_step_pin, False)
			GPIO.output(pan_step_pin, False)
			GPIO.output(tilt_step_pin, False)
		elif x % 2 == 0:
			GPIO.output(slide_step_pin, True)
			GPIO.output(pan_step_pin, True)
			time.sleep(0.0005)
			GPIO.output(slide_step_pin, False)
			GPIO.output(pan_step_pin, False)
		else:
			GPIO.output(slide_step_pin, True)
			time.sleep(0.0005)
			GPIO.output(slide_step_pin, False)
		time.sleep(0.0005)

	GPIO.output(slide_enable, False)
	GPIO.output(pan_enable, False)
	GPIO.output(tilt_enable, False)


def test_all():
	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	stepCount = 0
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00015)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00015)
		stepCount += 1
	GPIO.output(slide_enable, False)
	print("SLIDE Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	GPIO.output(pan_enable, True)
	GPIO.output(pan_dir_pin, LEFT)
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(pan_enable, False)
	print("PAN Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	GPIO.output(tilt_enable, True)
	GPIO.output(tilt_dir_pin, UP)
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(tilt_enable, False)
	print("TILT Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0


	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, AWAY)
	stepCount = 0
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00015)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00015)
		stepCount += 1
	GPIO.output(slide_enable, False)
	print("SLIDE Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0

	GPIO.output(pan_enable, True)
	GPIO.output(pan_dir_pin, RIGHT)
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(pan_enable, False)
	print("PAN Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0

	GPIO.output(tilt_enable, True)
	GPIO.output(tilt_dir_pin, DOWN)
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
		stepCount += 1
	GPIO.output(tilt_enable, False)
	print("TILT Steps Taken: " + str(stepCount))
	stepCount = 0


def test_step():
	print("stepping")
	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	for x in range(400):
		if stop():
			print("STOP BUTTON")
			break
		GPIO.output(slide_step_pin, True)
		time.sleep(0.001)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.001)
	GPIO.output(slide_dir_pin, AWAY)
	print("pause")
	time.sleep(1)
	for y in range(400):
		if stop():
			print("STOP BUTTON")
			break
		GPIO.output(slide_step_pin, True)
		time.sleep(0.001)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.001)
	GPIO.output(slide_enable, False)

def test_slide_altB():
	print("stepping")
	GPIO.output(slide_enable, True)
	GPIO.output(slide_dir_pin, HOME)
	stepCount = 0
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00015)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00015)
		stepCount += 1
	GPIO.output(slide_dir_pin, AWAY)
	print("Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(0.00025)
		GPIO.output(slide_step_pin, False)
		time.sleep(0.00025)
		stepCount += 1
	print("Steps Taken: " + str(stepCount))
	GPIO.output(slide_enable, False)

def set_slide_start():
	global programed_slide_steps
	stepCount = 0
	oppositeDir = not set_slide_direction
	GPIO.output(slide_dir_pin, oppositeDir)
	enable_slide()
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, False)
		time.sleep(set_slide_speed)
		stepCount += 1

	programed_slide_steps = stepCount
	GPIO.output(slide_dir_pin, set_slide_direction)
	disable_slide()
	print("START SLIDE SET: " + str(programed_slide_steps))


def set_slide_end():
	GPIO.output(slide_dir_pin, set_slide_direction)
	enable_slide()
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, False)
		time.sleep(set_slide_speed)

	disable_slide()

def slide_programed_test():
	GPIO.output(slide_dir_pin, set_slide_direction)
	enable_slide()
	for x in range(programed_slide_steps):
		if stop():
			break
		GPIO.output(slide_step_pin, True)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, False)
		time.sleep(set_slide_speed)

	disable_slide()


def jog_slide():
	GPIO.output(slide_dir_pin, set_slide_direction)
	enable_slide()
	while stop() == False:
		GPIO.output(slide_step_pin, True)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, False)
		time.sleep(set_slide_speed)

	disable_slide()

def test_pan_alt():
	print("stepping")
	GPIO.output(slide_enable, True)
	GPIO.output(pan_dir_pin, LEFT)
	for x in range(400):
		if stop():
			print("STOP BUTTON")
			break
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
	GPIO.output(pan_dir_pin, RIGHT)
	print("pause")
	time.sleep(1)
	for y in range(400):
		if stop():
			print("STOP BUTTON")
			break
		GPIO.output(pan_step_pin, True)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.001)
	GPIO.output(slide_enable, False)

def test_pan_altB():
	print("stepping")
	GPIO.output(pan_enable, True)
	GPIO.output(pan_dir_pin, LEFT)
	stepCount = 0
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(0.0005)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.0005)
		stepCount += 1
	GPIO.output(pan_dir_pin, RIGHT)
	print("Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(0.0005)
		GPIO.output(pan_step_pin, False)
		time.sleep(0.0005)
		stepCount += 1
	print("Steps Taken: " + str(stepCount))
	GPIO.output(pan_enable, False)


def set_pan_start():
	global programed_pan_steps
	stepCount = 0
	oppositeDir = not set_pan_direction
	GPIO.output(pan_dir_pin, oppositeDir)
	enable_pan()
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, False)
		time.sleep(set_pan_speed)
		stepCount += 1

	programed_pan_steps = stepCount
	GPIO.output(pan_dir_pin, set_pan_direction)
	disable_pan()
	print("START PAN SET: " + str(programed_pan_steps))


def set_pan_end():
	GPIO.output(pan_dir_pin, set_pan_direction)
	enable_pan()
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, False)
		time.sleep(set_pan_speed)

	disable_pan()

def pan_programed_test():
	GPIO.output(pan_dir_pin, set_pan_direction)
	enable_pan()
	for x in range(programed_pan_steps):
		if stop():
			break
		GPIO.output(pan_step_pin, True)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, False)
		time.sleep(set_pan_speed)

	disable_pan()


def jog_pan():
	GPIO.output(pan_dir_pin, set_pan_direction)
	enable_pan()
	while stop() == False:
		GPIO.output(pan_step_pin, True)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, False)
		time.sleep(set_pan_speed)

	disable_pan()

def test_tilt_alt():
	print("stepping")
	GPIO.output(slide_enable, True)
	GPIO.output(tilt_dir_pin, UP)
	for x in range(400):
		if stop():
			print("STOP BUTTON")
			break
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
	GPIO.output(tilt_dir_pin, DOWN)
	print("pause")
	time.sleep(1)
	for y in range(400):
		if stop():
			print("STOP BUTTON")
			break
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.001)
	GPIO.output(slide_enable, False)

def test_tilt_altB():
	print("stepping")
	GPIO.output(tilt_enable, True)
	GPIO.output(tilt_dir_pin, UP)
	stepCount = 0
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.0005)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.0005)
		stepCount += 1
	GPIO.output(tilt_dir_pin, DOWN)
	print("Steps Taken: " + str(stepCount))
	time.sleep(1)
	stepCount = 0
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(0.0005)
		GPIO.output(tilt_step_pin, False)
		time.sleep(0.0005)
		stepCount += 1
	print("Steps Taken: " + str(stepCount))
	GPIO.output(tilt_enable, False)



def set_tilt_start():
	global programed_tilt_steps
	stepCount = 0
	oppositeDir = not set_tilt_direction
	GPIO.output(tilt_dir_pin, oppositeDir)
	enable_tilt()
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(set_tilt_speed)
		GPIO.output(tilt_step_pin, False)
		time.sleep(set_tilt_speed)
		stepCount += 1

	programed_tilt_steps = stepCount
	GPIO.output(tilt_dir_pin, set_tilt_direction)
	disable_tilt()
	print("START TILT SET: " + str(programed_tilt_steps))


def set_tilt_end():
	GPIO.output(tilt_dir_pin, set_tilt_direction)
	enable_tilt()
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(set_tilt_speed)
		GPIO.output(tilt_step_pin, False)
		time.sleep(set_tilt_speed)

	disable_tilt()

def tilt_programed_test():
	GPIO.output(tilt_dir_pin, set_tilt_direction)
	enable_tilt()
	for x in range(programed_tilt_steps):
		if stop():
			break
		GPIO.output(tilt_step_pin, True)
		time.sleep(set_tilt_speed)
		GPIO.output(tilt_step_pin, False)
		time.sleep(set_tilt_speed)

	disable_tilt()


def jog_tilt():
	GPIO.output(tilt_dir_pin, set_tilt_direction)
	enable_tilt()
	while stop() == False:
		GPIO.output(tilt_step_pin, True)
		time.sleep(set_tilt_speed)
		GPIO.output(tilt_step_pin, False)
		time.sleep(set_tilt_speed)

	disable_tilt()


###### ----- Configure ----- #######

def change_slide_distance(distance):
	global set_slide_distance
	set_slide_distance = distance

def change_slide_direction(direction):
	global set_slide_direction
	
	if direction == 'home':
		set_slide_direction = HOME
	elif direction == 'away':
		set_slide_direction = AWAY
	else:
		print("INVALID DIR")

	GPIO.output(slide_dir_pin, set_slide_direction)

def change_slide_speed(speed):
	global set_slide_speed
	newSpeed = float(speed) / 10000.0
	set_slide_speed = newSpeed
	print("Slide Speed: " + str(newSpeed))

def slide_speed_setting(speed):
	global set_slide_speed
	if speed == 'slow':
		set_slide_speed = MEDIUM
	elif speed == 'medium':
		set_slide_speed = FAST
	elif speed == 'fast':
		set_slide_speed = TURBO
	else:
		print("INVALID SPEED")

def change_pan_degree(degree):
	global set_pan_degrees
	set_pan_degrees = degree

def change_pan_direction(direction):
	global set_pan_direction
	if direction == 'left':
		set_pan_direction = LEFT
	elif direction == 'right':
		set_pan_direction = RIGHT
	else:
		print("INVALID DIR")
	GPIO.output(pan_dir_pin, set_pan_direction)

def change_pan_speed(speed):
	global set_pan_speed
	newSpeed = float(speed) / 10000.0
	set_pan_speed = newSpeed
	print("Speed: " + str(newSpeed))

def pan_speed_setting(speed):
	global set_pan_speed
	if speed == 'slow':
		set_pan_speed = MEDIUM
	elif speed == 'medium':
		set_pan_speed = FAST
	elif speed == 'fast':
		set_pan_speed = TURBO
	else:
		print("INVALID SPEED")

def change_tilt_direction(direction):
	global set_tilt_direction
	if direction == 'up':
		set_tilt_direction = UP
	elif direction == 'down':
		set_tilt_direction = DOWN
	else:
		print("INVALID DIR")

	GPIO.output(tilt_dir_pin, set_tilt_direction)

def tilt_speed_setting(speed):
	global set_tilt_speed
	if speed == 'slow':
		set_tilt_speed = 0.002
	elif speed == 'medium':
		set_tilt_speed = 0.00075
	elif speed == 'fast':
		set_tilt_speed = 0.0002
	else:
		print("INVALID SPEED")

def change_tilt_speed(speed):
	global set_tilt_speed
	newSpeed = float(speed) / 10000.0
	set_tilt_speed = newSpeed
	print("Speed: " + str(newSpeed))





def change_step_mode(mode):
	global PAN_STEP_DEGREE
	global SLIDE_STEP_MM
	global step_mode_label
	if mode == 1:
		print("Full Steps")
		GPIO.output(M0, False)
		GPIO.output(M1, False)
		GPIO.output(M2, False)
		PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE
		SLIDE_STEP_MM = FULL_SLIDE_STEP_MM
		step_mode_label = "FULL STEPS"
	elif mode == 0.5:
		print("half steps")
		GPIO.output(M0, True)
		GPIO.output(M1, False)
		GPIO.output(M2, False)
		PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE * 2.0
		SLIDE_STEP_MM = FULL_SLIDE_STEP_MM * 2.0
		step_mode_label = "1/2 STEPS"

	elif mode == 0.25:
		print("Quarter Steps")
		GPIO.output(M0, False)
		GPIO.output(M1, True)
		GPIO.output(M2, False)
		PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE * 4.0
		SLIDE_STEP_MM = FULL_SLIDE_STEP_MM * 4.0
		step_mode_label = "1/4 STEPS"

	elif mode == 0.125:
		print("1/8 Steps")
		GPIO.output(M0, True)
		GPIO.output(M1, True)
		GPIO.output(M2, False)
		PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE * 8.0
		SLIDE_STEP_MM = FULL_SLIDE_STEP_MM * 8.0
		step_mode_label = "1/8 STEPS"

	else:
		print("Default: " + str(mode))
		#default to quarter steps
		GPIO.output(M0, False)
		GPIO.output(M1, True)
		GPIO.output(M2, False)
		PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE * 4.0
		SLIDE_STEP_MM = FULL_SLIDE_STEP_MM * 4.0
		step_mode_label = "1/4 STEPS"

	print("Slide steps: " + str(SLIDE_STEP_MM))
	print("Pan Steps: " + str(PAN_STEP_DEGREE))


def set_program_steps(totalSteps):
	global total_program_steps
	total_program_steps = totalSteps
	print("total: " + str(total_program_steps))





###### ----- Tests ----- #######
def test_slide_distance():
	GPIO.output(slide_enable, 1)
	steps = get_slide_steps(set_slide_distance)
	GPIO.output(slide_dir_pin, set_slide_direction)
	for x in range(steps):
		if checkLimits() == False:
			print("Limit Hit")
			time.sleep(1)
			reset_slide_limit(set_slide_speed)
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(set_slide_speed)
	GPIO.output(slide_enable, 0)


def test_pan_distance():
	GPIO.output(slide_enable, 1)
	steps = get_pan_steps(set_pan_degrees)
	GPIO.output(pan_dir_pin, set_pan_direction)
	for x in range(steps):
		GPIO.output(pan_step_pin, 1)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, 0)
		time.sleep(set_pan_speed)
	GPIO.output(slide_enable, 0)


def tilt_test():
	GPIO.output(slide_enable, 1)
	GPIO.output(tilt_dir_pin, 0)
	print("start")
	for x in range(1000):
		if check_tilt_limit() == False:
			print("tilt limit")
			break
		GPIO.output(tilt_step_pin, 1)
		time.sleep(0.0001)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(0.0001)

	GPIO.output(tilt_dir_pin, 1)
	print("change")
	time.sleep(1)
	for x in range(1000):
		if check_tilt_limit() == False:
			print("tilt limit")
			break
		GPIO.output(tilt_step_pin, 1)
		time.sleep(0.0001)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(0.0001)

	GPIO.output(slide_enable, 0)
	print("finished")


def tilt_home():
	enable_tilt()

	tilt_down()
	while tilt_status():
		GPIO.output(tilt_step_pin, 1)
		time.sleep(MEDIUM)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(MEDIUM)

	tilt_up()
	print("LIMIT")
	time.sleep(1)
	for x in range(TILT_OFFSET):
		if stop():
			break
		GPIO.output(tilt_step_pin, 1)
		time.sleep(FAST)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(FAST)

	GPIO.output(tilt_step_pin, set_tilt_direction)
	disable_tilt()


def pan_test():
	GPIO.output(slide_enable, 1)
	GPIO.output(pan_dir_pin, 0)
	print("start")
	for x in range(1000):
		if check_pan_limit() == False:
			break
		GPIO.output(pan_step_pin, 1)
		time.sleep(0.0001)
		GPIO.output(pan_step_pin, 0)
		time.sleep(0.0001)

	GPIO.output(pan_dir_pin, 1)
	print("change")
	time.sleep(1)
	for x in range(1000):
		if check_pan_limit() == False:
			break
		GPIO.output(pan_step_pin, 1)
		time.sleep(0.0001)
		GPIO.output(pan_step_pin, 0)
		time.sleep(0.0001)

	GPIO.output(slide_enable, 0)
	print("finished")


def pan_home():
	enable_pan()

	pan_right()
	while pan_status():
		GPIO.output(pan_step_pin, 1)
		time.sleep(MEDIUM)
		GPIO.output(pan_step_pin, 0)
		time.sleep(MEDIUM)

	pan_left()
	print("LIMIT")
	time.sleep(1)
	for x in range(PAN_OFFSET):
		if stop():
			break
		GPIO.output(pan_step_pin, 1)
		time.sleep(MEDIUM)
		GPIO.output(pan_step_pin, 0)
		time.sleep(MEDIUM)

	GPIO.output(pan_step_pin, set_pan_direction)
	disable_pan()



def slide_test():
	GPIO.output(slide_enable, 1)
	GPIO.output(slide_dir_pin, 0)
	print("start")
	for x in range(1000):
		if check_slide_limit() == False:
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(slide_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(slide_dir_pin, 1)
	print("change")
	time.sleep(1)
	for x in range(1000):
		if check_slide_limit() == False:
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(slide_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(slide_enable, 0)
	print("finished")



def slide_home():
	enable_slide()

	slide_dir_home()
	while slide_status():
		GPIO.output(slide_step_pin, 1)
		time.sleep(FAST)
		GPIO.output(slide_step_pin, 0)
		time.sleep(FAST)

	slide_away()
	print("LIMIT")
	time.sleep(1)
	for x in range(SLIDE_OFFSET):
		if stop():
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(FAST)
		GPIO.output(slide_step_pin, 0)
		time.sleep(FAST)

	GPIO.output(slide_step_pin, set_slide_direction)
	disable_slide()


def fast_home():
	enable_slide()
	enable_pan()
	enable_tilt()
	slide_dir_home()
	tilt_down()
	pan_right()

	findingHome = True
	while findingHome:
		if stop():
			break

		if slide_status() == False and pan_status() == False and tilt_status() == False:
			findingHome = False
			break	

		if slide_status():
			GPIO.output(slide_step_pin, 1)
		if pan_status():
			GPIO.output(pan_step_pin, 1)
		if tilt_status():
			GPIO.output(tilt_step_pin, 1)

		time.sleep(FAST)
		GPIO.output(slide_step_pin, 0)
		GPIO.output(pan_step_pin, 0)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(FAST)

	print("FOUND")
	time.sleep(1)

	tilt_up()
	pan_left()
	slide_away()

	for x in range(TILT_OFFSET):
		if stop():
			break
		if x < SLIDE_OFFSET:
			GPIO.output(slide_step_pin, 1)
		if x < PAN_OFFSET: 
			GPIO.output(pan_step_pin, 1)

		GPIO.output(tilt_step_pin, 1)
		time.sleep(FAST)
		GPIO.output(slide_step_pin, 0)
		GPIO.output(pan_step_pin, 0)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(FAST)

	disable_pan()
	disable_tilt()
	disable_slide()
	print("FINISHED")



def timelapse_home():
	slide_steps = 0
	pan_steps = 0
	tilt_steps = 0

	
	enable_pan()
	enable_tilt()
	
	tilt_down()
	pan_right()

	findingHome = True

	while findingHome:
		if stop():
			break

		if pan_status() == False and tilt_status() == False:
			findingHome = False
			break	

		if pan_status():
			GPIO.output(pan_step_pin, 1)
			pan_steps += 1
		if tilt_status():
			GPIO.output(tilt_step_pin, 1)
			tilt_steps += 1

		time.sleep(FAST)
		GPIO.output(pan_step_pin, 0)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(FAST)

	

	print("FOUND")
	time.sleep(1)

	tilt_up()
	pan_left()
	

	for x in range(TILT_OFFSET):
		if stop():
			break
		if x < PAN_OFFSET:
			GPIO.output(pan_step_pin, 1)
		GPIO.output(tilt_step_pin, 1)
		time.sleep(TURBO)
		GPIO.output(pan_step_pin, 0)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(TURBO)

	disable_pan()
	disable_tilt()
	slide_dir_home()
	enable_slide()


	while slide_status():
		if stop():
			break
		slide_steps += 1
		GPIO.output(slide_step_pin, 1)
		time.sleep(TURBO)
		GPIO.output(slide_step_pin, 0)
		time.sleep(TURBO)

	print("HOME")
	time.sleep(1)
	slide_away()
	for x in range(SLIDE_OFFSET):
		if stop():
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(TURBO)
		GPIO.output(slide_step_pin, 0)
		time.sleep(TURBO)

	
	disable_slide()
	print("FINISHED")
	print("SLIDE: " + str(slide_steps))
	print("PAN: " + str(pan_steps))
	print("TILT: " + str(tilt_steps))
###### ----- Step Conversions ----- #######

def get_slide_steps(distance):
	totalSteps = int(round(distance * SLIDE_STEP_MM))
	return totalSteps


def get_pan_steps(degrees):
	totalSteps = int(round(degrees * PAN_STEP_DEGREE))
	return totalSteps



###### ----- Setup ----- #######
def find_slide_home():
	if set_slide_direction == False:
		local_direction = True
	else:
		local_direction = False
	GPIO.output(slide_enable, 1)
	GPIO.output(slide_dir_pin, local_direction)
	while checkLimits():
		GPIO.output(slide_step_pin, 1)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(set_slide_speed)

	print("Limit Reached")
	time.sleep(0.5)
	GPIO.output(slide_dir_pin, set_slide_direction) #change direction
	steps = get_slide_steps(5) #move back 5mm
	for x in range(steps):
		GPIO.output(slide_step_pin, 1)
		time.sleep(set_slide_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(set_slide_speed)

	GPIO.output(slide_enable, 0)
	print("Finished")

def adjust_pan():
	if set_pan_direction == False:
		local_direction = True
	else:
		local_direction = False
	GPIO.output(slide_enable, 1)
	GPIO.output(pan_dir_pin, local_direction)
	steps = get_pan_steps(5) #move back 5mm
	for x in range(steps):
		GPIO.output(pan_step_pin, 1)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, 0)
		time.sleep(set_pan_speed)

	GPIO.output(pan_dir_pin, set_pan_direction)
	GPIO.output(slide_enable, 0)

def toggle_motor(motor):
	returnStatus = True
	global slide_active
	global pan_active
	global tilt_active

	if motor == 'slide':
		slide_active = not slide_active
		return slide_active
	elif motor == 'pan':
		pan_active = not pan_active
		return pan_active
	else:
		tilt_active = not tilt_active
		return tilt_active





	



###### ----- RUN PROGRAM ----- #######

def run_test_program():
	global pan_steps_cycle
	global slide_steps_cycle
	global slide_to_pan_ratio
	total_slide_steps = get_slide_steps(set_slide_distance)
	total_pan_steps = get_pan_steps(set_pan_degrees)
	print("Total slide: " + str(total_slide_steps))
	print("Total pan: " + str(total_pan_steps))
	pan_steps_cycle = int(round(total_pan_steps / total_program_steps))
	slide_steps_cycle = int(round(total_slide_steps / total_program_steps))
	print("Pan/cycle: " + str(pan_steps_cycle))
	print("Slide/cycle: " + str(slide_steps_cycle))
	local_cycle_count = 0
	slide_to_pan_ratio = slide_steps_cycle / pan_steps_cycle
	print("Ratio: " + str(slide_to_pan_ratio))
	while local_cycle_count < total_program_steps:
		if checkLimits() == False:
			print("stopped by limits")
			break
		single_movement_cycle()
		local_cycle_count += 1
	print("finished: " + str(local_cycle_count))
	GPIO.output(slide_enable, 0)




def single_movement_cycle():
	GPIO.output(slide_enable, 1)
	for x in range(slide_steps_cycle):
		if checkLimits() == False:
			break
		if x < 1:
			single_dual_step(set_slide_speed)
		elif x % slide_to_pan_ratio == 0:
			single_dual_step(set_slide_speed)
		else:
			single_slide_step(set_slide_speed)



def set_timelapse_step_values():
	global pan_steps_cycle
	global slide_steps_cycle
	global slide_to_pan_ratio
	global program_cycle_count
	program_cycle_count = 0
	total_slide_steps = get_slide_steps(set_slide_distance)
	total_pan_steps = get_pan_steps(set_pan_degrees)
	print("Total slide: " + str(total_slide_steps))
	print("Total pan: " + str(total_pan_steps))
	pan_steps_cycle = int(round(total_pan_steps / total_program_steps))
	slide_steps_cycle = int(round(total_slide_steps / total_program_steps))
	print("Pan/cycle: " + str(pan_steps_cycle))
	print("Slide/cycle: " + str(slide_steps_cycle))
	local_cycle_count = 0
	slide_to_pan_ratio = slide_steps_cycle / pan_steps_cycle
	print("Ratio: " + str(slide_to_pan_ratio))




def set_pan_dir(dir):
	GPIO.output(pan_dir_pin, dir)

def pan_step_on():
	GPIO.output(pan_step_pin, 1)

def pan_step_off():
	GPIO.output(pan_step_pin, 0)


def set_slide_dir(dir):
	GPIO.output(slide_dir_pin, dir)

def slide_step_on():
	GPIO.output(slide_step_pin, 1)

def slide_step_off():
	GPIO.output(slide_step_pin, 0)	


def move_stepper(steps, step_speed, direction):
	GPIO.output(slide_enable, 1)
	GPIO.output(slide_dir_pin, direction)
	for x in range(steps):
		GPIO.output(slide_step_pin, 1)
		time.sleep(step_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(step_speed)
	GPIO.output(slide_enable, 0)


def stepMotors():
	step_count = 200
	GPIO.output(slide_enable, 1)
	for x in range(step_count):
		GPIO.output(slide_step_pin, 1)
		time.sleep(0.005)
		GPIO.output(slide_step_pin, 0)
		time.sleep(0.005)

	for x in range(step_count):
		GPIO.output(pan_step_pin, 1)
		time.sleep(0.005)
		GPIO.output(pan_step_pin, 0)
		time.sleep(0.005)

	GPIO.output(slide_enable, 0)








###### ----- Limits ----- #######


def reset_slide():
	reset_direction = set_slide_direction
	set_slide_direction = not set_slide_direction
	change_slide_direction(set_slide_direction)
	for x in range(400):
		single_slide_step(quick_slide_speed)
	change_slide_direction(reset_direction)

def reset_pan():
	reset_direction = set_pan_direction
	set_pan_direction = not set_pan_direction
	change_pan_direction(set_pan_direction)
	for x in range(400):
		single_pan_step(quick_pan_speed)
	change_pan_direction(reset_direction)

def reset_tilt():
	reset_direction = set_tilt_direction
	set_tilt_direction = not set_tilt_direction
	change_tilt_direction(set_tilt_direction)
	for x in range(400):
		single_tilt_step(quick_tilt_speed)
	change_tilt_direction(reset_direction)


def checkLimits():
	limitStatus = True
	if check_slide_limit() == False:
		limitStatus = False
	elif check_pan_limit() == False:
		limitStatus = False
	elif check_tilt_limit() == False:
		limitStatus = False

	return limitStatus


def check_slide_limit():
	limitStatus = True
	left_end = GPIO.input(slide_limit_left)
	right_end = GPIO.input(slide_limit_right)
	if left_end == False:
		limitStatus = False
	if right_end == False:
		limitStatus = False
	return limitStatus


def check_pan_limit():
	limitStatus = True
	pan_status = GPIO.input(pan_limit)

	if pan_status == False:
		limitStatus = False

	return limitStatus

def check_tilt_limit():
	limitStatus = True
	tilt_status = GPIO.input(tilt_limit)

	if tilt_status == False:
		limitStatus = False

	return limitStatus

def tilt_status():
	# Returns false if limit hit
	if GPIO.input(stop_button) == False:
		print("exit by stop")
		return False
	else:
		return GPIO.input(tilt_limit)

def pan_status():
	# Returns false if limit hit
	if GPIO.input(stop_button) == False:
		print("exit by stop")
		return False
	else:
		return GPIO.input(pan_limit)

def slide_status():
	limitStatus = True
	left_end = GPIO.input(slide_limit_left)
	right_end = GPIO.input(slide_limit_right)
	if left_end == False:
		limitStatus = False
	if right_end == False:
		limitStatus = False
	if GPIO.input(stop_button) == False:
		print("exit by stop")
		limitStatus = False
	return limitStatus

def stop():
	limitStatus = False
	stop_status = GPIO.input(stop_button)
	
	if stop_status == False:
		print("-----EXIT BUTTON-----")
		limitStatus = True

	return limitStatus


def check_inputs():
	enable_tilt()
	enable_pan()

	while stop() == False:

		if GPIO.input(joystick_down) == False:
			print("JOYSTICK AAAAA")
			tilt_down()
			GPIO.output(tilt_step_pin, True)
			time.sleep(set_tilt_speed)
			GPIO.output(tilt_step_pin, False)
			time.sleep(set_tilt_speed)

		if GPIO.input(joystick_up) == False:
			print("JOYSTICK BBBBB")
			tilt_up()
			GPIO.output(tilt_step_pin, True)
			time.sleep(set_tilt_speed)
			GPIO.output(tilt_step_pin, False)
			time.sleep(set_tilt_speed)

		if GPIO.input(joystick_left) == False:
			print("JOYSTICK CCCCC")
			pan_left()
			GPIO.output(pan_step_pin, True)
			time.sleep(set_pan_speed)
			GPIO.output(pan_step_pin, False)
			time.sleep(set_pan_speed)

		if GPIO.input(joystick_right) == False:
			print("JOYSTICK left")
			pan_right()
			GPIO.output(pan_step_pin, True)
			time.sleep(set_pan_speed)
			GPIO.output(pan_step_pin, False)
			time.sleep(set_pan_speed)
			

	print("EXITING")
	disable_tilt()
	disable_pan()

		










###### ----- Motor Control ----- #######

def slide_on():
	GPIO.output(slide_step_pin, 1)

def slide_off():
	GPIO.output(slide_step_pin, 0)


def pan_on():
	GPIO.output(pan_step_pin, 1)

def pan_off():
	GPIO.output(pan_step_pin, 0)


def tilt_on():
	GPIO.output(tilt_step_pin, 1)

def tilt_off():
	GPIO.output(tilt_step_pin, 0)

def toggle_motor(motor):
	global slide_active
	global pan_active
	global tilt_active

	if motor == "slide":
		slide_active = not slide_active
	elif motor == "pan":
		pan_active = not pan_active
	elif motor == "tilt":
		tilt_active = not tilt_active
	else:
		print("invalid")




def single_pan_step(speed):
	GPIO.output(pan_step_pin, 1)
	time.sleep(speed)
	GPIO.output(pan_step_pin, 0)
	time.sleep(speed)

def single_slide_step(speed):
	GPIO.output(slide_step_pin, 1)
	time.sleep(speed)
	GPIO.output(slide_step_pin, 0)
	time.sleep(speed)

def single_tilt_step(speed):
	GPIO.output(tilt_step_pin, 1)
	time.sleep(speed)
	GPIO.output(tilt_step_pin, 0)
	time.sleep(speed)

def move_slide(distance):
	enable()
	total_steps = int(SLIDE_STEP_MM * distance)
	for x in range(total_steps):
		if check_slide_limit() == False:
			reset_slide()
			break
		single_slide_step(quick_slide_speed)
	disable()

def move_pan(degrees):
	enable()
	total_steps = int(PAN_STEP_DEGREE * degrees)
	for x in range(total_steps):
		if check_pan_limit() == False:
			reset_pan()
			break
		single_pan_step(quick_pan_speed)
	disbale()

def move_tilt(degrees):
	total_steps = int(TILT_STEP_DEGREE * degrees)
	for x in range(total_steps):
		if check_tilt_limit() == False:
			reset_tilt()
			break
		single_slide_step(quick_tilt_speed)
	disable()

def enable():
	GPIO.output(slide_enable, 1)

def disable():
	GPIO.output(slide_enable, 0)



def enable_tilt():
	GPIO.output(tilt_enable, True)

def disable_tilt():
	GPIO.output(tilt_enable, False)

def tilt_down():
	GPIO.output(tilt_dir_pin, DOWN)

def tilt_up():
	GPIO.output(tilt_dir_pin, UP)


def enable_pan():
	GPIO.output(pan_enable, True)

def disable_pan():
	GPIO.output(pan_enable, False)

def pan_left():
	GPIO.output(pan_dir_pin, LEFT)

def pan_right():
	GPIO.output(pan_dir_pin, RIGHT)

def enable_slide():
	GPIO.output(slide_enable, True)

def disable_slide():
	GPIO.output(slide_enable, False)

def slide_dir_home():
	GPIO.output(slide_dir_pin, HOME)

def slide_away():
	GPIO.output(slide_dir_pin, AWAY)
	

def cleanup():
	GPIO.cleanup()
	pass
























