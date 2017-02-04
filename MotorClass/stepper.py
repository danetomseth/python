import RPi.GPIO as GPIO ## Import GPIO library
from decimal import Decimal
import time
import analog
import motor
from subprocess import call






slide_pins = [17, 4, 27]
pan_pins = [23, 24, 25]
tilt_pins = [20, 21, 12]

slide_home = False
pan_home = False
tilt_home = True

slide_away = True
pan_away = True
tilt_away = False


stop_button = 22
limits = [5, 6, 13, 19]

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    

GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
for y in limits:
    GPIO.setup(y, GPIO.IN, pull_up_down=GPIO.PUD_UP) 




#Create motor Classes
#([step, dir, enable], step_mode, step_angle, ratio, analog_pin, [limits], home_dir, steps_from_home, motor_name): #pins [step, dir, enable]
slide = motor.MotorObj(slide_pins, 4, 0.131, 3.54331, 2, [5,6], slide_home, 3000, "slide")
pan = motor.MotorObj(pan_pins, 8, 0.094, 4.2, 0, [19], pan_home, 70000, "pan")
tilt = motor.MotorObj(tilt_pins, 8, 0.035, 1, 1, [13], tilt_home, 3500, "tilt")


all_motors = [slide, pan, tilt]



def slide_joystick():
    slide.enable()
    while stop() == False and slide.limit():
        slide.read_analog()
        if slide.analog_speed == 0:
            pass
        else:
            for x in range(400):
                slide.variable_single_step()
    slide.disable()

def all_axis_joystick():
    print("READING")
    # motors = [slide, pan, tilt]
    motors = [pan, tilt]

    time_count = 0.0001
    for motor in motors:
        motor.enable()

    while stop() == False:

        if Decimal(str(time_count)) % Decimal('0.1') == Decimal('0.0'):
            for motor in motors:
                motor.read_analog()
        for motor in motors:
            if (motor.analog_speed > 0):
                if Decimal(str(time_count)) % Decimal(str(motor.analog_speed)) == Decimal('0.0'):
                    motor.alt_step()
        time.sleep(0.0001)
        time_count += 0.0001

    for motor in motors:
        motor.disable()

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
        motor.read_analog()
        if motor.analog_speed == 0:
            pass
        else:
            for x in range(100):
                motor.variable_single_step()
    motor.disable()
    time.sleep(1)

    time.sleep(0.5)
    print("FINSIHED")

def set_B():
    motors = [slide, pan, tilt]

    for motor in motors:
        motor.enable_counting()
        while stop() == False:
            motor.read_analog()
            if motor.analog_speed == 0:
                pass
            else:
                for x in range(100):
                    motor.variable_single_step()
        motor.disable_counting()
        time.sleep(1)
    time.sleep(0.5)
    print("FINISHED")
    print("Steps per motor: ")
    for motor in motors:
        print(motor.name + " steps: " + str(motor.step_count))
        time.sleep(1)



def return_all_home():
    motors = [slide, pan, tilt]

    for motor in motors:
        motor.return_home()

def tilt_sweep():
    tilt.set_direction(tilt_away)
    for x in range(3):
        if stop():
            return
        print("Tilt: " + str(x))
        time.sleep(0.5)
        take_picture()
        tilt.move_distance(10)
    take_picture()
    tilt.set_direction(tilt_home)
    tilt.move_distance(30)
    print("TILT DONE")

def pan_sweep(tilt_active):
    pan.set_direction(pan_home)
    for x in range(5):
        if stop():
            return
        if tilt_active:
            tilt_sweep()
        else:
            time.sleep(0.25)
            take_picture()
        pan.move_distance(18)
    take_picture()
    print("MOVE DONE")

def pano_test():
    local_motors = [slide, pan]
    print("STARTING")
    pan.set_direction(pan_away)
    slide.set_direction(slide_away)
    
    pan.move_distance(45)

    for x in range(5):
        if stop():
            print("BREAKING A")
            return
        pan_sweep(False)
        pan.set_direction(pan_away)

        slide.enable()
        pan.enable()

        slide.set_step_count(50)
        pan.set_step_count(90)

        both_finished = False
        while both_finished == False:
            if stop():
                x = 10
                print("BREAKING B")
                break
            both_finished = True
            if slide.program_finished == False:
                slide.programmed_alt_step()
                both_finished = False
            if pan.program_finished == False:
                pan.programmed_alt_step()
                both_finished = False
            time.sleep(0.0001)
            if slide.program_finished == False:
                slide.programmed_alt_step()
            if pan.program_finished == False:
                pan.programmed_alt_step()
            time.sleep(0.0001)
        print("MOVE #: "+str(x))
    print("FINISHED")



def pano_tilt():
    print("STARTING")
    pan.set_direction(pan_away)
    slide.set_direction(slide_away)
    tilt.set_direction(tilt_away)
    
    pan.move_distance(45)

    for x in range(5):
        if stop():
            print("BREAKING A")
            break
        pan_sweep(True)
        pan.set_direction(pan_away)

        slide.enable()
        pan.enable()
        # tilt.enable()

        slide.set_step_count(50)
        pan.set_step_count(90)

        both_finished = False
        while both_finished == False:
            if stop():
                x = 10
                print("BREAKING B")
                break
            both_finished = True
            if slide.program_finished == False:
                slide.programmed_alt_step()
                both_finished = False
            if pan.program_finished == False:
                pan.programmed_alt_step()
                both_finished = False
            time.sleep(0.0001)
            if slide.program_finished == False:
                slide.programmed_alt_step()
            if pan.program_finished == False:
                pan.programmed_alt_step()
            time.sleep(0.0001)
        print("MOVE #: "+str(x))
    print("FINISHED")


        

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
        pan.find_home()
    elif motor == 'tilt':
        tilt.find_home()
    else:
        print("Invalid Motor")

def adjust_home(motor):
    if motor == 'slide':
        slide.adjust_home()
    elif motor == 'pan':
        pan.adjust_home()
    elif motor == 'tilt':
        tilt.adjust_home()
    else:
        print("Invalid Motor")


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
    call (["gphoto2","--capture-image"])


def limit_test():
    while stop() == False:
        for x in limits:
            if GPIO.input(x) == False:
                print("INPUT: " + str(x))
                time.sleep(0.5)
            else:
                pass

    print("FINISHED")

def clean():
    GPIO.cleanup()
    pass




