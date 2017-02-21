

import RPi.GPIO as GPIO ## Import GPIO library
from decimal import Decimal
import time
import analog
import stepperClass as stepper
from main import window
from subprocess import call
from kivy.uix.progressbar import ProgressBar
from cameraClass import camera





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
interval_steps = 0
timelapse_active = False

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
# camera = CameraObj()


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
        for x in range(5):
            for motor in active_motors:
                motor.count_step_high()
            time.sleep(0.0001)
            for motor in active_motors:
                motor.step_low()
            time.sleep(0.0001)

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

        for x in range(5):
            for motor in active_motors:
                motor.step_high()
            time.sleep(0.0001)
            for motor in active_motors:
                motor.step_low()
            time.sleep(0.0001)
    camera.capture_image()

    


def timelapse_preview():
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


def reset_position():
    motors = sorted_motors
    for motor in motors:
        motor.switch_direction()
        motor.enable()
    time.sleep(0.25)
    for x in range(motors[2].programmed_steps):
        if stop():
            break
        elif x < motors[0].programmed_steps:
            motors[0].step_high()
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(0.00015)
            motors[0].step_low()
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(0.00015)

        elif x < motors[1].programmed_steps:
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(0.00015)
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(0.00015)

        else:
            motors[2].step_high()
            time.sleep(0.00015)
            motors[2].step_low()
            time.sleep(0.00015)

    for motor in motors:
        motor.disable()
        motor.switch_direction()

    print("ALL FINISHED")


def program_timelapse():
    global interval_steps
    global timelapse_active
    timelapse_active = True
    motors = sorted_motors
    print("TOTAL PICTURES: " + str(camera.total_pictures))
    print("STEPS PER PIC")
    for motor in motors:
        motor.set_move_steps(camera.total_pictures)

    interval_steps = motors[2].steps_per_move
    print("Max steps: " + str(interval_steps))

def reset_timelapse():
    global timelapse_active
    global sorted_motors
    sorted_motors = []
    timelapse_active = False
    motors = [slide, pan, tilt]
    camera.picture_count = 0
    for motor in motors:
        motor.programmed_steps = 0


def timelapse_step():
    global timelapse_active
    motors = [slide, pan, tilt]
    step_speed = 0.001
    for motor in motors:
        motor.enable()

    for x in range(interval_steps):
        if stop():
            camera.picture_count = camera.total_pictures
            timelapse_active = False
            break
        if x < 20:
            step_speed -= 0.000025
        for motor in motors:
            motor.step_high()
        time.sleep(step_speed)
        for motor in motors:
            if motor.timelapse_step_low(x) == False:
                motors.remove(motor)
        time.sleep(step_speed)

    for motor in motors:
        motor.disable()
    camera.timelapse_picture()





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


def slide_pan_joystick():
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


def run():
    stop_status = GPIO.input(stop_button)
    if stop_status == False:
        print("-----EXIT BUTTON-----")
        return stop_status
    else:
        return stop_status

def stop():
    limitStatus = False
    stop_status = GPIO.input(stop_button)
    
    if stop_status == False:
        limitStatus = True
        disable_all()

    return limitStatus

def disable_all():
    for motor in all_motors:
        motor.disable()






def clean():
    GPIO.cleanup()
    pass




