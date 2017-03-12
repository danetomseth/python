import RPi.GPIO as GPIO ## Import GPIO library
import time






stop_button = 22







output_List = [14]

txd_pin = 14
rxd_pin = 15


last_state = False


def gpio_setup():
    # GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    GPIO.setmode(GPIO.BCM) ## Use board pin numbering
    print("Setting Up")
    GPIO.setup(stop_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
    
    GPIO.setup(rxd_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
    GPIO.setup(txd_pin, GPIO.OUT)
    GPIO.output(txd_pin, 0)


    print("Setup Finished")


def shutter():
    total_time = 0
    for x in range(10):
        start = time.time()
        GPIO.output(txd_pin, True)
        time.sleep(0.166667)
        GPIO.output(txd_pin, False)
        end = time.time() - start
        total_time += end
        print(str(end))
        time.sleep(2)        
    print("FINISHED")
    total_time = total_time / 10.0
    print(str(total_time))

def test():
    global last_state
    last_state = not last_state
    start = time.time()
    GPIO.output(txd_pin, last_state)
    end = time.time() - start
    print(str(end))
    print(last_state)

def read_txd():
    for x in range(100):
        pin_stat = GPIO.input(txd_pin)
        print(pin_stat)
        time.sleep(0.1)
    print("FINISHED")

def read_rxd():
    for x in range(100):
        pin_stat = GPIO.input(rxd_pin)
        print(pin_stat)
        time.sleep(0.1)
    print("FINISHED")

def read_stop():
    for x in range(50):
        pin_stat = GPIO.input(stop_button)
        print(pin_stat)
        time.sleep(0.1)
    print("FINISHED")


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
