import RPi.GPIO as GPIO ## Import GPIO library
import time
import threading




#Stepper vars
slide_step_pin = 16
slide_dir_pin = 12

pan_step_pin = 20
pan_dir_pin = 21


tilt_step_pin = 19
tilt_dir_pin = 26

enable_pin = 25

servo_pin = 18

slide_limit_left = 6
slide_limit_right = 13

pan_limit = 4
tilt_limit = 5


#Step mode pins
M0 = 22
M1 = 27
M2 = 17

output_List = [slide_dir_pin, slide_step_pin, pan_dir_pin, pan_step_pin, tilt_dir_pin, tilt_step_pin, enable_pin, M0, M1, M2]

# Constants
LEFT = False
RIGHT = True

FULL_PAN_STEP_DEGREE = 62.69 #number of steps/degree for pan

FULL_SLIDE_STEP_MM = 13.4983  #number of steps/mm for slider

PAN_STEP_DEGREE = FULL_PAN_STEP_DEGREE * 4.0
SLIDE_STEP_MM = FULL_SLIDE_STEP_MM * 4.0

step_mode_label = "1/4 STEPS"

#### ---- user variables ---- ####

#-----PAN
set_pan_degrees = 20
set_pan_direction = LEFT
set_pan_speed = 0.001
pan_steps_cycle = 5

pan_home_set = False
pan_start_set = False


#-----SLIDE
set_slide_distance = 200
set_slide_direction = LEFT
set_slide_speed = 0.001
slide_steps_cycle = 25

activeStepping = False
last_servo_position = 5
slide_speed = 0.01


#-----Program
total_program_steps = 1200
slide_to_pan_ratio = 5
program_cycle_count = 0


slide_direction = LEFT
pan_direction = LEFT

# step_size = 100
GPIO.setmode(GPIO.BCM) ## Use board pin numbering

GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18, 100)
servo.start(5)


def gpio_setup():
	# GPIO.setmode(GPIO.BCM) ## Use board pin numbering
	GPIO.setup(slide_limit_left, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(slide_limit_right, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(tilt_limit, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	GPIO.setup(pan_limit, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
	for x in output_List:
		GPIO.setup(x, GPIO.OUT) ##setup gpio as out
		GPIO.output(x, False) ##set initial state to low

	change_step_mode(0.25)

def motor_on_off():
	moveMotor(DC_slide_L)

def run_servo():
	servo.ChangeDutyCycle(2.5)  # turn towards 0 degree
	time.sleep(1) # sleep 1 second
	servo.ChangeDutyCycle(12.5) # turn towards 180 degree
	time.sleep(1) # sleep 1 second 
	servo.stop()


###### ----- Motor Control ----- #######
def servo_position(angle):
	global last_servo_position
	duty = float(angle) / 10.0 + 2.5
	last_servo_position = angle
	servo.ChangeDutyCycle(duty)

def variable_slide_step(step_speed, steps):
	step_count = int(steps)
	GPIO.output(enable_pin, 1)
	GPIO.output(slide_dir_pin, slide_direction)
	for x in range(step_count):
		if checkLimits() == False:
			print("Limit Hit")
			time.sleep(1)
			reset_slide_limit(step_speed)
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(step_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(step_speed)
	GPIO.output(enable_pin, 0)

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

def single_dual_step(speed):
	GPIO.output(slide_step_pin, 1)
	GPIO.output(pan_step_pin, 1)
	time.sleep(speed)
	GPIO.output(pan_step_pin, 0)
	GPIO.output(slide_step_pin, 0)

def ramp_slide_step(step_speed, steps):
	step_count = int(steps)
	GPIO.output(enable_pin, 1)
	GPIO.output(slide_dir_pin, slide_direction)
	start_speed = 0.03
	while start_speed > step_speed:
		GPIO.output(slide_step_pin, 1)
		time.sleep(start_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(start_speed)
		if step_count % 2 == 0:
			start_speed = start_speed - 0.001
		step_count -= 1
		print(step_count)
		print(start_speed)
	for x in range(step_count):
		if checkLimits() == False:
			print("Limit Hit")
			time.sleep(1)
			reset_slide_limit(step_speed)
			break
		GPIO.output(slide_step_pin, 1)
		time.sleep(step_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(step_speed)
	GPIO.output(enable_pin, 0)

def variable_pan_step(step_speed, steps):
	step_count = int(steps)
	GPIO.output(enable_pin, 1)
	GPIO.output(pan_dir_pin, pan_direction)
	for x in range(step_count):
		GPIO.output(pan_step_pin, 1)
		time.sleep(step_speed)
		GPIO.output(pan_step_pin, 0)
		time.sleep(step_speed)
	GPIO.output(enable_pin, 0)


###### ----- Configure ----- #######


def change_pan_degree(degree):
	global set_pan_degrees
	set_pan_degrees = degree

def change_pan_direction(direction):
	global set_pan_direction
	set_pan_direction = direction
	GPIO.output(pan_dir_pin, set_pan_direction )

def change_pan_speed(speed):
	global set_pan_speed
	newSpeed = float(speed) / 10000.0
	set_pan_speed = newSpeed
	print("Speed: " + str(newSpeed))

def change_slide_distance(distance):
	global set_slide_distance
	set_slide_distance = distance

def change_slide_direction(direction):
	global set_slide_direction
	set_slide_direction = direction
	GPIO.output(slide_dir_pin, set_slide_direction)

def change_slide_speed(speed):
	global set_slide_speed
	newSpeed = float(speed) / 10000.0
	set_slide_speed = newSpeed
	print("Slide Speed: " + str(newSpeed))


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
	GPIO.output(enable_pin, 1)
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
	GPIO.output(enable_pin, 0)


def test_pan_distance():
	GPIO.output(enable_pin, 1)
	steps = get_pan_steps(set_pan_degrees)
	GPIO.output(pan_dir_pin, set_pan_direction)
	for x in range(steps):
		GPIO.output(pan_step_pin, 1)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, 0)
		time.sleep(set_pan_speed)
	GPIO.output(enable_pin, 0)


def tilt_test():
	GPIO.output(enable_pin, 1)
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

	GPIO.output(enable_pin, 0)
	print("finished")


def tilt_home():
	GPIO.output(enable_pin, 1)
	GPIO.output(tilt_dir_pin, 0)
	print("start")
	while check_tilt_limit() == True:
		GPIO.output(tilt_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(tilt_dir_pin, 1)
	print("change")
	time.sleep(1)
	while check_tilt_limit() == True:
		GPIO.output(tilt_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(tilt_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(enable_pin, 0)
	print("finished")



def pan_test():
	GPIO.output(enable_pin, 1)
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

	GPIO.output(enable_pin, 0)
	print("finished")


def pan_home():
	GPIO.output(enable_pin, 1)
	GPIO.output(pan_dir_pin, 0)
	print("start")
	while check_pan_limit() == True:
		GPIO.output(pan_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(pan_dir_pin, 1)
	print("change")
	time.sleep(1)
	while check_pan_limit() == True:
		GPIO.output(pan_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(pan_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(enable_pin, 0)
	print("finished")



def slide_test():
	GPIO.output(enable_pin, 1)
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

	GPIO.output(enable_pin, 0)
	print("finished")



def slide_home():
	GPIO.output(enable_pin, 1)
	GPIO.output(slide_dir_pin, 1)
	print("start")
	while check_slide_limit() == True:
		GPIO.output(slide_step_pin, 1)
		time.sleep(0.001)
		GPIO.output(slide_step_pin, 0)
		time.sleep(0.001)

	GPIO.output(slide_dir_pin, 0)
	print("change")
	time.sleep(1)
	for x in range(1500):
		GPIO.output(slide_step_pin, 1)
		time.sleep(0.0005)
		GPIO.output(slide_step_pin, 0)
		time.sleep(0.0005)

	GPIO.output(enable_pin, 0)
	print("finished")



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
	GPIO.output(enable_pin, 1)
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

	GPIO.output(enable_pin, 0)
	print("Finished")

def adjust_pan():
	if set_pan_direction == False:
		local_direction = True
	else:
		local_direction = False
	GPIO.output(enable_pin, 1)
	GPIO.output(pan_dir_pin, local_direction)
	steps = get_pan_steps(5) #move back 5mm
	for x in range(steps):
		GPIO.output(pan_step_pin, 1)
		time.sleep(set_pan_speed)
		GPIO.output(pan_step_pin, 0)
		time.sleep(set_pan_speed)

	GPIO.output(pan_dir_pin, set_pan_direction)
	GPIO.output(enable_pin, 0)



###### ----- Limits ----- #######
def reset_slide_limit(step_speed):
	global slide_direction
	GPIO.output(enable_pin, 1)
	if slide_direction == False:
		slide_direction = True
		GPIO.output(slide_dir_pin, slide_direction)
	else:
		slide_direction = False
		GPIO.output(slide_dir_pin, slide_direction)

	for x in range(100):
		GPIO.output(slide_step_pin, 1)
		time.sleep(step_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(step_speed)

	GPIO.output(enable_pin, 1)




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
	GPIO.output(enable_pin, 0)


# def single_movement_cycle():
# 	pan_steps_taken = 0
# 	GPIO.output(enable_pin, 1)
# 	for x in range(slide_steps_cycle):
# 		if checkLimits() == False:
# 			break
# 		if pan_steps_taken < pan_steps_cycle:
# 			single_dual_step(set_slide_speed)
# 			pan_steps_taken += 1
# 		else:
# 			single_slide_step(set_slide_speed)

def single_movement_cycle():
	GPIO.output(enable_pin, 1)
	for x in range(slide_steps_cycle):
		if checkLimits() == False:
			break
		if x < 1:
			single_dual_step(set_slide_speed)
		elif x % slide_to_pan_ratio == 0:
			single_dual_step(set_slide_speed)
		else:
			single_slide_step(set_slide_speed)
	# GPIO.output(enable_pin, 0)



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


def timelapse_program():
	global program_cycle_count

	if checkLimits() == False:
		print("returned false limits")
		GPIO.output(enable_pin, 0)
		return False

	single_movement_cycle()
	program_cycle_count += 1

	if program_cycle_count > 100:
		print("Returned false program cycle")
		GPIO.output(enable_pin, 0)
		return False
	else:
		return True


def start_servo():
	servo.start(5)

def stop_servo():
	servo.ChangeDutyCycle(0)

def set_pan_dir(dir):
	GPIO.output(pan_dir_pin, dir)

def pan_step_on():
	GPIO.output(pan_step_pin, 1)

def pan_step_off():
	GPIO.output(pan_step_pin, 0)


# def change_slide_direction(direction):
# 	global slide_direction
# 	slide_direction = direction
# 	print("direction: " + str(slide_direction))

# def change_pan_direction(direction):
# 	global pan_direction
# 	pan_direction = direction
# 	print("direction: " + str(pan_direction))




def set_slide_dir(dir):
	GPIO.output(slide_dir_pin, dir)

def slide_step_on():
	GPIO.output(slide_step_pin, 1)

def slide_step_off():
	GPIO.output(slide_step_pin, 0)	

def toggle_stepper(step_speed):
	print("start")

	# servo.stop()

def move_stepper(steps, step_speed, direction):
	GPIO.output(enable_pin, 1)
	GPIO.output(slide_dir_pin, direction)
	for x in range(steps):
		GPIO.output(slide_step_pin, 1)
		time.sleep(step_speed)
		GPIO.output(slide_step_pin, 0)
		time.sleep(step_speed)
	GPIO.output(enable_pin, 0)

def run_cycle_f(step_speed):
	for x in range(10):
		move_stepper(10, step_speed, RIGHT)
		servo_angle = last_servo_position + 2
		servo_position(servo_angle)
	servo.ChangeDutyCycle(0)

def run_cycle_r(step_speed):
	for x in range(10):
		move_stepper(10, step_speed, LEFT)
		servo_angle = last_servo_position - 2
		servo_position(servo_angle)
	servo.ChangeDutyCycle(0)

def stepMotors():
	step_count = 200
	GPIO.output(enable_pin, 1)
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

	GPIO.output(enable_pin, 0)





def enable_stepper():
	GPIO.output(enable_pin, 1)

def disable_stepper():
	GPIO.output(enable_pin, 0)
	

def cleanup():
	GPIO.cleanup()
	pass



###### ----- Limits ----- #######

def check_left_limit():
	left_end = GPIO.input(slide_limit_left)
	if left_end == False:
		return True
	else:
		return False

def check_right_limit():
	right_end = GPIO.input(slide_limit_right)
	if right_end == False:
		return True
	else:
		return False

def checkLimits():
	limitStatus = True
	left_end = GPIO.input(slide_limit_left)
	right_end = GPIO.input(slide_limit_right)
	if left_end == False:
		limitStatus = False
	if right_end == False:
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




def check_all_limits():
	for x in range(100):
		pan_status = GPIO.input(pan_limit)
		tilt_status = GPIO.input(tilt_limit)
		left_status = GPIO.input(slide_limit_left)
		right_status = GPIO.input(slide_limit_right)

		if pan_status == False:
			print("pan!!")
			break
		if tilt_status == False:
			print("Tilt")
			break
		if left_status == False: 
			print("LEFT")
			break
		if right_status == False:
			print("right")
			break

		time.sleep(0.1)

	print("Not checking")























