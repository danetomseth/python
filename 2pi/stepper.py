

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

#Microstep pins
slide_M0 = 16
slide_M1 = 18
pan_M1 = 26

micropins = [slide_M0, slide_M1, pan_M1]

step_count_list = []
sorted_motors = []
interval_steps = 0
timelapse_active = False

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    

GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for p in micropins:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

for y in limits:
    GPIO.setup(y, GPIO.IN, pull_up_down=GPIO.PUD_UP) 




#Create motor Classes
#([step, dir, enable], step_mode, step_angle, ratio, analog_pin, [limits], main_direction, home_dir, steps_from_home, motor_name): #pins [step, dir, enable]
slide = stepper.MotorObj(slide_pins, 4, 0.131, 3.54331, 2, [5,6], True, slide_home, 3000, "slide")
pan = stepper.MotorObj(pan_pins, 8, 0.094, 4.2, 0, [19], True, pan_home, 4000, "pan")
tilt = stepper.MotorObj(tilt_pins, 8, 0.035, 2, 1, [13], False, tilt_home, 3250, "tilt")


#Create Camera
# camera = CameraObj()

# ------CONSTANTS-------
steps_read_cycle = 60
all_motors = [slide, pan, tilt]


def change_step(step):
    if step == 0:
        print("FULL")
        for pin in micropins:
            GPIO.output(pin, False)
    elif step == 1:
        GPIO.output(slide_M0, True)
        GPIO.output(slide_M1, False)
        print("HALF")
    elif step == 2:
        GPIO.output(slide_M0, False)
        GPIO.output(slide_M1, True)
        print("QUARTER")
    elif step == 3:
        GPIO.output(slide_M0, True)
        GPIO.output(slide_M1, True)
        print("EIGHTH")
    else:
        GPIO.output(pan_M1, True)
        print("PAN 32")


def change_pan_step(mode):
    if mode == 16:
        GPIO.output(pan_M1, False)
    elif mode == 32:
        GPIO.output(pan_M1, True)

def change_slide_step(step):
    if step == 1:
        print("FULL")
        GPIO.output(slide_M0, False)
        GPIO.output(slide_M1, False)
    elif step == 2:
        GPIO.output(slide_M0, True)
        GPIO.output(slide_M1, False)
        print("HALF")
    elif step == 4:
        GPIO.output(slide_M0, False)
        GPIO.output(slide_M1, True)
        print("QUARTER")
    elif step == 8:
        GPIO.output(slide_M0, True)
        GPIO.output(slide_M1, True)
        print("EIGHTH")

def change_dir():
    while stop() == False:
        for motor in all_motors:
            motor.switch_direction()
        time.sleep(1)

def test_pan():
    print("STARTING")
    pan.enable()
    while stop() == False:
        pan.single_step_speed(0.0002)
    pan.disable()
    print("FINISHED")




def set_timelapse_start():
    global step_count_list
    global sorted_motors
    sorted_motors = []
    speed_list = []
    speed = 0.0001
    
    for motor in all_motors:
        motor.read_debounce()
        motor.start_counting()
    
    while stop() == False:
        active_motors = []
        for motor in all_motors:
            motor.read_debounce()
            if motor.analog_speed == 1000:
                pass
            else:
                speed_list.append(motor.analog_speed)
                active_motors.append(motor)
        if len(active_motors) > 0:
            speed = min(speed_list)
            speed_list = []
            for x in range(steps_read_cycle):
                for motor in active_motors:
                    motor.count_step_high()
                time.sleep(speed)
                for motor in active_motors:
                    motor.step_low()
                time.sleep(speed)
    
    for motor in all_motors:
        motor.program_steps()
        step_count_list.append(motor.programmed_steps)
    
    step_count_list.sort()
    
    for x in step_count_list:
        for motor in all_motors:
            if motor.programmed_steps == x:
                sorted_motors.append(motor)
    
    return sorted_motors

def set_timelapse_end():
    speed_list = []
    speed = 0.0001
    for motor in all_motors:
        motor.read_debounce()
    while stop() == False:
        active_motors = []
        for motor in all_motors:
            motor.read_debounce()
            if motor.analog_speed == 1000:
                pass
            else:
                speed_list.append(motor.analog_speed)
                active_motors.append(motor)
        if len(active_motors) > 0:
            speed = min(speed_list)
            speed_list = []
            for x in range(steps_read_cycle):
                for motor in active_motors:
                    motor.step_high()
                time.sleep(speed)
                for motor in active_motors:
                    motor.step_low()
                time.sleep(speed)
    disable_all()

def timelapse_preview():
    motors = sorted_motors
    counts = [0,0,0]
    preview_speed = 0.005
    enable_all()
    for x in range(motors[2].programmed_steps):
        if preview_speed > 0.00015:
            preview_speed -= 0.000005
        if stop():
            break
        elif x < motors[0].programmed_steps:
            motors[0].step_high()
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(preview_speed)
            motors[0].step_low()
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(preview_speed)

        elif x < motors[1].programmed_steps:
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(preview_speed)
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(preview_speed)

        else:
            motors[2].step_high()
            time.sleep(preview_speed)
            motors[2].step_low()
            time.sleep(preview_speed)

    disable_all()



def reset_position():
    motors = sorted_motors
    preview_speed = 0.005
    for motor in motors:
        motor.switch_direction()
        motor.enable()
    time.sleep(0.25)
    for x in range(motors[2].programmed_steps):
        if preview_speed > 0.001:
            preview_speed -= 0.00005
        if stop():
            break
        elif x < motors[0].programmed_steps:
            motors[0].step_high()
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(preview_speed)
            motors[0].step_low()
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(preview_speed)

        elif x < motors[1].programmed_steps:
            motors[1].step_high()
            motors[2].step_high()
            time.sleep(preview_speed)
            motors[1].step_low()
            motors[2].step_low()
            time.sleep(preview_speed)

        else:
            motors[2].step_high()
            time.sleep(preview_speed)
            motors[2].step_low()
            time.sleep(preview_speed)

    for motor in motors:
        motor.disable()
        motor.switch_direction()

    print("ALL FINISHED")


def program_timelapse():
    global interval_steps
    global timelapse_active
    timelapse_active = True
    print("TOTAL PICTURES: " + str(camera.total_pictures))
    print("STEPS PER PIC")
    for motor in sorted_motors:
        motor.set_move_steps(camera.total_pictures)

    interval_steps = sorted_motors[2].steps_per_move
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
    time.sleep(0.05)
    for x in range(interval_steps):
        if stop():
            camera.picture_count = camera.total_pictures
            timelapse_active = False
            break
        for motor in motors:
            motor.step_high()
        time.sleep(step_speed)
        for motor in motors:
            if motor.timelapse_step_low(x) == False:
                motors.remove(motor)
        time.sleep(step_speed)

    for motor in motors:
        motor.disable()
    # if camera.connected:
    #     camera.timelapse_picture()





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

def enable_run():
    time.sleep(1)
    print("SLIDE")
    while stop() == False:
        slide.enable()
    slide.disable()
    time.sleep(1)
    print("PAN")
    while stop() == False:
        pan.enable()
    pan.disable()
    time.sleep(1)
    print("TILT")
    while stop() == False:
        tilt.enable()
    tilt.disable()




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

def enable_all():
    for motor in all_motors:
        motor.enable()






def clean():
    GPIO.cleanup()
    pass




