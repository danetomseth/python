import RPi.GPIO as GPIO ## Import GPIO library
import time




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




def gpio_setup():
    # GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    print("Setting Up")
    GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out

    for x in output_List:
        GPIO.setup(x, GPIO.OUT) ##setup gpio as out
        GPIO.output(x, False) ##set initial state to low

    print("Setup Finished")




def run_A(speed):
    global last_A
    GPIO.output(driverA_enable, True)
    GPIO.output(driverA_dir, last_A)
    print("Moving B")
    time.sleep(0.05)
    for x in range(3000):
        if stop():
            break

        GPIO.output(driverA_step, True)
        time.sleep(speed)
        GPIO.output(driverA_step, False)
        time.sleep(speed)
    last_A = not last_A
    GPIO.output(driverA_enable, False)


def run_B(speed):
    global last_B
    GPIO.output(driverB_enable, True)
    GPIO.output(driverB_dir, last_B)
    print("Moving B")

    time.sleep(0.05)
    for x in range(3000):
        if stop():
            break

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
        if stop():
            break
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


def clean():
    GPIO.cleanup()
    pass
