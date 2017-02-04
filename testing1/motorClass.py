#!/usr/bin/env python

# Slide motor
#   step = 17
#   dir = 4
#   enable = 27
#   gearing = 13.73
#   step_angle = 0.131
#   current = 1.68A


# Pan Motor
#   step = 23
#   dir = 24
#   enable = 25
#   gearing = 19.19
#   step_angle = 0.094
#   current = 0.8A 

# Tilt Motor
#   step = 20
#   dir = 21
#   enable = 12
#   gearing = 50.9
#   step_angle = 0.035
#   current = 0.8A  

from time import sleep
import RPi.GPIO as GPIO

class Motor(object):
    def __init__(self, pins, step_mode, step_angle): #pins [step, dir, enable]
        self.step_pin = pins[0]
        self.direction_pin = pins[1]
        self.enable = pins[2]
        self.step_mode = step_mode
        self.deg_per_step = step_angle / step_mode  
        self.steps_per_rev = int(360 / self.deg_per_step)
        self.speed = 0.00025
        self.enabled = False  
        
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

    def _set_rpm(self, rpm):
        """Set the turn speed in RPM."""
        self._rpm = rpm
        # T is the amount of time to stop between signals
        self._T = (60.0 / rpm) / self.steps_per_rev

    # This means you can set "rpm" as if it is an attribute and
    # behind the scenes it sets the _T attribute
    rpm = property(lambda self: self._rpm, _set_rpm)

    def step_amount(self, steps, direction):
        for x in range(steps):
            GPIO.output(self.step_pin, True)
            time.sleep(self.speed)
            GPIO.output(self.step_pin, False)
            time.sleep(self.speed)

    def single_step(self):
        GPIO.output(self.step_pin, True)
        time.sleep(self.speed)
        GPIO.output(self.step_pin, False)
        time.sleep(self.speed)

    def set_speed(self, speed):
        self.speed = speed

    
    def set_direction(self, direction):
        GPIO.output(self.direction, direction)

    def enable(self):
        GPIO.output(enable_pin, True)        

    def disable(self):
        GPIO.output(enable_pin, False)        

    def toggle_enable(self):
        self.enabled = not self.enabled

    def __clear(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    m = Motor([18,22,24,26])
    m.rpm = 5
    print "Pause in seconds: " + `m._T`
    m.move_to(90)
    sleep(1)
    m.move_to(0)
    sleep(1)
    m.mode = 2
    m.move_to(90)
    sleep(1)
    m.move_to(0)
    GPIO.cleanup()