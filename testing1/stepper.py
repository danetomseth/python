import RPi.GPIO as GPIO ## Import GPIO library
import time
import analog
import limits as limits









driverA_step = 17
driverA_dir = 4
driverA_enable = 27


driverB_step = 20
driverB_dir = 21
driverB_enable = 12


driverC_step = 23
driverC_dir = 24
driverC_enable = 25

stop_button = 22

last_A = True
last_B = True
last_C = True





output_List = [driverA_step, driverA_dir, driverA_enable, driverB_step, driverB_dir, driverB_enable, driverC_step, driverC_dir, driverC_enable]


limits = [5, 6, 13, 19]




def gpio_setup():
    # GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    print("Setting Up")
    GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
    for x in output_List:
        GPIO.setup(x, GPIO.OUT) ##setup gpio as out
        GPIO.output(x, False) ##set initial state to low

    for y in limits:
        GPIO.setup(y, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out

    print("Setup Finished")


def run_limit_test(speed):
    GPIO.output(driverA_enable, True)
    GPIO.output(driverA_dir, True)
    for x in range(2000):
        single_slide_step(speed)

    GPIO.output(driverA_dir, False)
    time.sleep(1)

    for x in range(2000):
        single_slide_step(speed)

    # while check_slide():
    #     if stop():
    #         break
    #     else:
    #         single_slide_step(speed)

    # print("SWITCHING")

    # time.sleep(1)

    # reset_slide(True, speed)
    # print("Disengaged")

    # time.sleep(1)

    # while check_slide():
    #     if stop():
    #         break
    #     else:
    #         single_slide_step(speed)

    # time.sleep(1)

    # reset_slide(True, speed)
    # print("Disengaged")

    # time.sleep(1)

    # while check_slide() == False:
    #     single_slide_step(speed)
             
    GPIO.output(driverA_enable, False)
    print("FINISHED")




def slide_joystick():
    GPIO.output(driverA_enable, True)
    while stop() == False:
        speed_read = analog.read_channel(1)
        if speed_read == 0:
            pass
        else:
            if speed_read < 0:
                GPIO.output(driverA_dir, True)
            else:
                GPIO.output(driverA_dir, False)
            speed_read = abs(speed_read)
            step_slide(400, speed_read)
    GPIO.output(driverA_enable, False)

def test_slide():
    GPIO.output(driverA_enable, True)
    while stop() == False:
        speed_read = analog.read_channel(2)

        if speed_read == 0:
            pass
        else:
            if speed_read < 0:
                GPIO.output(driverA_dir, True)
            else:
                GPIO.output(driverA_dir, False)
            speed_read = abs(speed_read)
            for x in range(100):
                GPIO.output(driverA_step, True)
                time.sleep(speed_read)
                GPIO.output(driverA_step, False)
                time.sleep(speed_read)
    GPIO.output(driverA_enable, False)


def test_pan():
    GPIO.output(driverC_enable, True)
    while stop() == False:
        speed_read = analog.read_channel(0)

        if speed_read == 0:
            pass
        else:
            if speed_read < 0:
                GPIO.output(driverC_dir, True)
            else:
                GPIO.output(driverC_dir, False)
            speed_read = abs(speed_read)
            for x in range(100):
                GPIO.output(driverC_step, True)
                time.sleep(speed_read)
                GPIO.output(driverC_step, False)
                time.sleep(speed_read)
    GPIO.output(driverC_enable, False)


def test_tilt():
    GPIO.output(driverB_enable, True)
    while stop() == False:
        speed_read = analog.read_channel(1)

        if speed_read == 0:
            pass
        else:
            if speed_read < 0:
                GPIO.output(driverB_dir, True)
            else:
                GPIO.output(driverB_dir, False)
            speed_read = abs(speed_read)
            for x in range(100):
                GPIO.output(driverB_step, True)
                time.sleep(speed_read)
                GPIO.output(driverB_step, False)
                time.sleep(speed_read)
    GPIO.output(driverB_enable, False)

def run_A(speed):
    GPIO.output(driverA_enable, True)
    while stop() == False:
        speed_read = analog.read_channel(1)

        if speed_read == 0:
            pass
        elif abs(speed_read) < 0.0001:
            print("too fast")
            pass
        else:
            print("stepping: " + str(speed_read))
            if speed_read < 0:
                GPIO.output(driverA_dir, True)
                print("LEFT")
            else:
                GPIO.output(driverA_dir, False)
                print("right")

            GPIO.output(driverA_step, True)
            time.sleep(speed_read)
            GPIO.output(driverA_step, False)
            time.sleep(speed_read)
    GPIO.output(driverA_enable, False)

    # GPIO.output(driverA_enable, True)
    # GPIO.output(driverA_dir, True)
    # print("Moving A")
    # print("Speed: " + str(speed))
    # time.sleep(0.05)
    # for x in range(1000):
    #     GPIO.output(driverA_step, True)
    #     time.sleep(speed)
    #     GPIO.output(driverA_step, False)
    #     time.sleep(speed)
    # print("Switching")
    # GPIO.output(driverA_dir, False)
    # time.sleep(0.5)
    # for x in range(1000):
    #     GPIO.output(driverA_step, True)
    #     time.sleep(speed)
    #     GPIO.output(driverA_step, False)
    #     time.sleep(speed)
    # GPIO.output(driverA_enable, False)
    # print("Finished")


def run_B(speed):
    global last_B
    GPIO.output(driverB_enable, True)
    GPIO.output(driverB_dir, last_B)
    print("Moving B")

    time.sleep(0.05)
    for x in range(3000):
        GPIO.output(driverB_step, True)
        time.sleep(speed)
        GPIO.output(driverB_step, False)
        time.sleep(speed)
    last_B = not last_B
    GPIO.output(driverB_enable, False)



def run_C(speed):
    global last_C
    GPIO.output(driverC_enable, True)
    GPIO.output(driverC_dir, last_C)
    print("Moving C")
    time.sleep(0.05)
    for x in range(3000):
        GPIO.output(driverC_step, True)
        time.sleep(speed)
        GPIO.output(driverC_step, False)
        time.sleep(speed)
    last_C = not last_C
    GPIO.output(driverC_enable, False)




def enable_all():
    GPIO.output(driverA_enable, True)
    GPIO.output(driverB_enable, True)
    GPIO.output(driverC_enable, True)



def disable_all():
    GPIO.output(driverA_enable, False)
    GPIO.output(driverB_enable, False)
    GPIO.output(driverC_enable, False)


def stop():
    limitStatus = False
    stop_status = GPIO.input(stop_button)
    
    if stop_status == False:
        print("-----EXIT BUTTON-----")
        limitStatus = True

    return limitStatus


def check_slide():
    if GPIO.input(5) == False:
        # print("LIMIT MOTOR")
        return False
    elif GPIO.input(6) == False:
        # print("LIMIT AWAY")
        return False
    else:
        return True

def reset_slide(last_direction, speed):
    move_direction = not last_direction
    GPIO.output(driverA_dir, move_direction)
    step_slide(500, speed)


def single_slide_step(speed):
        GPIO.output(driverA_step, True)
        time.sleep(speed)
        GPIO.output(driverA_step, False)
        time.sleep(speed)

def step_slide(steps, speed):
    for x in range(steps):
        if stop() == False:
            pass
        else: 
            GPIO.output(driverA_step, True)
            time.sleep(speed)
            GPIO.output(driverA_step, False)
            time.sleep(speed)



def reset_pan(last_direction, speed):
    move_direction = not last_direction
    GPIO.output(driverB_dir, move_direction)
    step_pan(500, speed)


def single_pan_step(speed):
        GPIO.output(driverB_step, True)
        time.sleep(speed)
        GPIO.output(driverB_step, False)
        time.sleep(speed)

def step_pan(steps, speed):
    for x in range(steps):
        if stop() == False:
            pass
        else: 
            GPIO.output(driverB_step, True)
            time.sleep(speed)
            GPIO.output(driverB_step, False)
            time.sleep(speed)

def clean():
    GPIO.cleanup()
    pass
