

import RPi.GPIO as GPIO ## Import GPIO library
from decimal import Decimal
import time
import analog
import stepperClass as stepper
import cameraClass
from subprocess import call
from kivy.uix.progressbar import ProgressBar





slide_pins = [17, 4, 27]
pan_pins = [23, 24, 25]
tilt_pins = [20, 21, 12]

slide_home = False
pan_home = True
tilt_home = True

slide_away = True
pan_away = True
tilt_away = False


stop_button = 22
limits = [5, 6, 13, 19]

step_count_list = []
sorted_motors = []

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    

GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
for y in limits:
    GPIO.setup(y, GPIO.IN, pull_up_down=GPIO.PUD_UP) 




#Create motor Classes
#([step, dir, enable], step_mode, step_angle, ratio, analog_pin, [limits], main_direction, home_dir, steps_from_home, motor_name): #pins [step, dir, enable]
slide = stepper.MotorObj(slide_pins, 4, 0.131, 3.54331, 2, [5,6], True, slide_home, 3000, "slide")
pan = stepper.MotorObj(pan_pins, 8, 0.094, 4.2, 0, [19], True, pan_home, 4000, "pan")
tilt = stepper.MotorObj(tilt_pins, 8, 0.035, 2, 1, [13], False, tilt_home, 3250, "tilt")


#Create Camera
camera = cameraClass.CameraObj()


all_motors = [slide, pan, tilt]




def control_all():
    motors = [pan, tilt, slide]
    # motors = [slide]
    for motor in motors:
        motor.enable()
        motor.start_counting()
        motor.read_joystick()
    time_stamp = 0.0001
    time_start = time.time()
    while stop() == False:
        active_motors = []
        for motor in motors:
            motor.read_joystick()
            if motor.analog_speed == 1000:
                pass
            else:
                active_motors.append(motor)

        step_stamp = 1
        for x in range(12):
            for motor in active_motors:
                if step_stamp % motor.analog_speed == 0:
                    motor.alt_step()
            step_stamp += 1
            time.sleep(0.000075)



    print("FINISHED")

def time_test():
    print("TIME TEST")
    time.sleep(0.5)
    time_total = 0
    count = 0

    slide.enable()
    pan.enable()
    while stop() == False:
        # motor.read_analog()
        slide.read_two_motor()
        if slide.analog_speed == 0:
            pass
        else:
            for x in range(5):
                slide.two_motor_step()
    time.sleep(1)
    take_picture()

    print("FINSIHED")


def joystick_step_count():
    motors = [pan, tilt, slide]
    # motors = [slide]
    for motor in motors:
        motor.enable()
        motor.start_counting()
        motor.read_joystick()
    time_stamp = 0.0001
    time_start = time.time()
    while stop() == False:
        active_motors = []
        for motor in motors:
            motor.read_joystick()
            if motor.analog_speed == 1000:
                pass
            else:
                active_motors.append(motor)

        step_stamp = 1
        

        for x in range(10):
            for motor in active_motors:
                motor.count_step_high()
            time.sleep(0.0001)
            for motor in active_motors:
                motor.step_low()
            time.sleep(0.0001)



def joystick_set_start():
    global step_count_list
    global sorted_motors
    motors = [pan, tilt, slide]
    # motors = [slide]
    for motor in motors:
        motor.enable()
        motor.start_counting()
        motor.read_joystick()
    time_stamp = 0.0001
    time_start = time.time()
    while stop() == False:
        active_motors = []
        for motor in motors:
            motor.read_joystick()
            if motor.analog_speed == 1000:
                pass
            else:
                active_motors.append(motor)
        for x in range(10):
            for motor in active_motors:
                motor.count_step_high()
            time.sleep(0.0002)
            for motor in active_motors:
                motor.step_low()
            time.sleep(0.0002)

    for motor in motors:
        motor.program_steps()
        step_count_list.append(motor.programmed_steps)

    step_count_list.sort()
    sorted_motors = []
    for x in step_count_list:
        print("SORTED: " + str(x))
        for motor in motors:
            if motor.programmed_steps == x:
                print("ADD: " + motor.name)
                sorted_motors.append(motor)
    for x in sorted_motors:
        print(x.name)


def joystick_set_end():
    motors = [pan, tilt, slide]
    for motor in motors:
        motor.enable()
        motor.read_joystick()
    while stop() == False:
        active_motors = []
        for motor in motors:
            motor.read_joystick()
            if motor.analog_speed == 1000:
                pass
            else:
                active_motors.append(motor)

        for x in range(10):
            for motor in active_motors:
                motor.count_step_high()
            time.sleep(0.0002)
            for motor in active_motors:
                motor.step_low()
            time.sleep(0.0002)

    print("DONE")
    

def set_A(set_motor):
    if set_motor == 'slide':
        motor = slide
    elif set_motor == 'pan':
        motor = pan
    elif set_motor == 'tilt':
        motor = tilt
    else:
        print("Invalid Motor")
        return
    motor.enable()
    while stop() == False:
        # motor.read_analog()
        motor.read_set_channel()
        if motor.analog_speed == 0:
            pass
        else:
            for x in range(5):
                motor.variable_single_step()
    motor.disable()
    time.sleep(1)
    take_picture()

    print("FINSIHED")


def set_timelapse_B(move_motor):
    print(move_motor)

def set_B(move_motor):
    if move_motor == 'slide':
        motor = slide
    elif move_motor == 'pan':
        motor = pan
    elif move_motor == 'tilt':
        motor = tilt
    else:
        print("Invalid Motor")
        return
    motor.enable_counting()
    while stop() == False:
        motor.read_set_channel()
        if motor.analog_speed == 0:
            pass
        else:
            for x in range(50):
                motor.variable_single_step()
    motor.disable_counting()
    time.sleep(1)
    print(motor.name + " steps: " + str(motor.step_count))


def run_timelapse_preview():
    motors = sorted_motors
    counts = [0,0,0]
    for motor in motors:
        motor.enable()
    print("STARTING")
    time.sleep(1)
    for x in range(motors[2].programmed_steps):
        if stop():
            break
        elif x < motors[0].programmed_steps:
            counts[0] += 1
            counts[1] += 1
            counts[2] += 1
            motors[0].step_high()
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(0.00015)
            motors[0].step_low()
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(0.00015)

        elif x < motors[1].programmed_steps:
            counts[1] += 1
            counts[2] += 1
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(0.00015)
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(0.00015)

        else:
            counts[2] += 1
            motors[2].step_high()
            time.sleep(0.00015)
            motors[2].step_low()
            time.sleep(0.00015)

    for motor in motors:
        motor.disable()

    for count in counts:
        print("STEPS: " + str(count))
    time.sleep(1)
    print("ALL FINISHED")


def run_AB():
    motors = sorted_motors
    for motor in motors:
        motor.enable()
    print("STARTING")
    time.sleep(1)
    for motor in motors:
        motor.enable()
        time.sleep(0.025)
        for x in range(motor.programmed_steps):
            if stop():
                print("STOPPING")
                break
            else:
                motor.single_step()
        motor.disable()
        print(motor.name + " FINISHED")
    time.sleep(1)
    print("ALL FINISHED")



def return_all_home():
    motors = [slide, pan, tilt]

    for motor in motors:
        motor.return_home()

def move(motor):
    if motor == 'slide':
        slide.joystick()
    elif motor == 'pan':
        pan.joystick()
    elif motor == 'tilt':
        tilt.joystick()
    else:
        print("Invalid Motor")

def move_distance(motor, distance):
    if motor == 'slide':
        slide.move_distance(distance)
    elif motor == 'pan':
        pan.move_distance(distance)
    elif motor == 'tilt':
        tilt.move_distance(distance)
    else:
        print("Invalid Motor")

def find_home(motor):
    if motor == 'slide':
        slide.find_home()
    elif motor == 'pan':
        print("FINDING PAN HOME")
        pan.find_home()
    elif motor == 'tilt':
        tilt.find_home()
    else:
        print("Invalid Motor")

def find_home_all():
    motors = [slide, pan, tilt]
    home_speed = 0.0003
    for motor in motors:
        motor.set_home_direction()
        motor.enable()
    step_count = 0
    limits_reached = 0
    while limits_reached < 3:
        limits_reached = 0
        if stop():
            break            
        for motor in motors:
            if motor.check_home_limit():
                motor.step_high()
            else:
                limits_reached += 1
        time.sleep(home_speed)
        for motor in motors:
            motor.step_low()
        time.sleep(home_speed)
        step_count += 1
    for motor in motors:
        motor.switch_direction()

    if stop():
        limits_reached = 3
    else:
        limits_reached = 0
    print("step count: " + str(step_count))
    time.sleep(1)
    step_count = 0
    

    while limits_reached < 3:
        limits_reached = 0
        if stop():
            break            
        for motor in motors:
            if step_count < motor.home_step_offset:
                motor.step_high()
            else:
                limits_reached += 1
        time.sleep(home_speed)
        for motor in motors:
            motor.step_low()
        time.sleep(home_speed)
        step_count += 1

    for motor in motors:
        motor.disable()
    print("FINISHED")

def home_speed_offset():
    motors = [slide, pan, tilt]
    slow_motors = [pan, tilt]
    home_speed = 0.00025
    for motor in motors:
        motor.set_home_direction()
        motor.enable()
    step_count = 0
    limits_reached = 0
    while limits_reached < 3:
        limits_reached = 0
        if stop():
            break
        if step_count % 4 == 0:            
            for motor in slow_motors:
                if motor.check_home_limit():
                    motor.step_high()
                else:
                    limits_reached += 1
        if slide.check_home_limit():
            slide.step_high()
        else:
            limits_reached += 1
        time.sleep(home_speed)
        if step_count % 4 == 0:
            for motor in slow_motors:
                motor.step_low()
        slide.step_low()
        time.sleep(home_speed)
        step_count += 1
    for motor in motors:
        motor.switch_direction()

    if stop():
        limits_reached = 3
    else:
        limits_reached = 0
    print("step count: " + str(step_count))
    time.sleep(1)
    step_count = 0
    

    while limits_reached < 3:
        limits_reached = 0
        if stop():
            break            
        for motor in motors:
            if step_count < motor.home_step_offset:
                motor.step_high()
            else:
                limits_reached += 1
        time.sleep(home_speed)
        for motor in motors:
            motor.step_low()
        time.sleep(home_speed)
        step_count += 1

    for motor in motors:
        motor.disable()
    print("FINISHED")


def read_channel(motor):
    while stop() == False:
        if motor == 'slide':
            slide.read_analog()
        elif motor == 'pan':
            pan.read_analog()
        elif motor == 'tilt':
            tilt.read_analog()
        else:
            print("Invalid Motor")
        time.sleep(0.1)


def stop():
    limitStatus = False
    stop_status = GPIO.input(stop_button)
    
    if stop_status == False:
        # print("-----EXIT BUTTON-----")
        limitStatus = True
        disable_all()

    return limitStatus

def disable_all():
    for motor in all_motors:
        motor.disable()

    print("DISABLED ALL")

def run():
    stop_status = GPIO.input(stop_button)
    if stop_status == False:
        print("-----EXIT BUTTON-----")
        return stop_status
    else:
        return stop_status


def take_picture():
    print("PICTURE!")
    # call (["gphoto2","--capture-image"])


def clean():
    GPIO.cleanup()
    pass




