import RPi.GPIO as GPIO ## Import GPIO library
import time
import stepper

limit_pins = [5, 6, 13, 19]



def read_all():
    while stepper.stop() == False:
        for x in limit_pins:
            status = GPIO.input(x)
            if status == False:
                print("LIMIT: " + str(x))
        time.sleep(0.25)
    print("FINISHED")


def check_slide():
    if GPIO.input(5) == False:
        print("LIMIT MOTOR")
        return False
    elif GPIO.input(6) == False:
        print("LIMIT AWAY")
        return False
    else:
        return True
