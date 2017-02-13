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

import time
import RPi.GPIO as GPIO
import analog
import control

class MotorObj(object):
    def __init__(self, pins, step_mode, step_angle, ratio, analog_pin, limits, home_dir, steps_from_home, motor_name): #pins [step, dir, enable]
        self.name = motor_name
        self.step_pin = pins[0]
        self.direction_pin = pins[1]
        self.enable_pin = pins[2]

        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)
        


        self.step_mode = step_mode
        self.deg_per_step = step_angle / (step_mode)

        self.unit_per_step = (self.deg_per_step / ratio)

        self.steps_per_rev = int(360 / self.deg_per_step)
        self.units_per_rev = int(self.unit_per_step * self.steps_per_rev)
        
        print(self.name + ": " + str(self.steps_per_rev))



        self.speed = 0.00015
        self.analog_speed = 0.0
        self.enabled = False
        self.analog_pin = analog_pin 
        self.step_state = False

        self.current_direction = home_dir
        self.home_direction = home_dir
        self.home_step_offset = steps_from_home

        self.step_count = 0
        self.programmed_steps = 0
        self.programmed_steps_taken = 0
        self.program_finished = False
        self.display_message = True


        self.limits = limits 
        self.limit_status = False
        
        

        for l in limits:
           GPIO.setup(l, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.set_direction(self.home_direction) 

    def _set_rpm(self, rpm):
        """Set the turn speed in RPM."""
        self._rpm = rpm
        # T is the amount of time to stop between signals
        self._T = (60.0 / rpm) / self.steps_per_rev

    # This means you can set "rpm" as if it is an attribute and
    # behind the scenes it sets the _T attribute
    rpm = property(lambda self: self._rpm, _set_rpm)

    def move(self, steps):
        self.enable()
        time.sleep(0.01)
        for x in range(steps):
            GPIO.output(self.step_pin, True)
            time.sleep(self.speed)
            GPIO.output(self.step_pin, False)
            time.sleep(self.speed)
        self.disable()


    def move_distance(self, distance):
        total_steps = int(distance / self.unit_per_step)
        self.enable()
        print("Steps: " + str(total_steps))
        for steps in range(total_steps):
            if self.limit() == False:
                break
            if control.stop():
                break
            else:
                self.single_step()
        self.disable()

    def set_step_count(self, distance):
        self.program_finished = False
        self.display_message = True
        self.programmed_steps_taken = 0
        self.programmed_steps = int(distance / self.unit_per_step)
        print(self.name + " STEPS PROGRAMMED: " + str(self.programmed_steps))



    def joystick(self):
        self.enable()
        while control.run() and self.limit():
            self.read_analog()
            if self.analog_speed == 0:
                pass
            else:
                for x in range(400):
                    self.variable_single_step()
        self.disable()

    def single_step(self):
        GPIO.output(self.step_pin, True)
        time.sleep(self.speed)
        GPIO.output(self.step_pin, False)
        time.sleep(self.speed)
      

    def step_high(self):
        GPIO.output(self.step_pin, True)

    def step_low(self):
        GPIO.output(self.step_pin, False)

    def alt_step(self):
        self.step_state = not self.step_state
        GPIO.output(self.step_pin, self.step_state)


    def programmed_alt_step(self):
        if (self.programmed_steps_taken / 2) < self.programmed_steps:
            if self.limit() == False:
                self.programmed_steps_taken = self.programmed_steps * 2
                self.program_finished = True
                if self.display_message:
                    print(self.name + " STOPPING BY STEP ADJUST")
                    self.display_message = False
                    self.disable()
            else:
                self.step_state = not self.step_state
                GPIO.output(self.step_pin, self.step_state)
                self.programmed_steps_taken += 1
        else:
            self.program_finished = True
            if self.display_message:
                print(self.name + " STOPPING BY STEP ADJUST")
                self.display_message = False
                self.disable()




    def set_speed(self, speed):
        self.speed = speed

    def set_direction(self, direction):
        self.current_direction = direction
        GPIO.output(self.direction_pin, direction)

    def switch_direction(self):
        self.current_direction = not self.current_direction
        GPIO.output(self.direction_pin, self.current_direction)

    def read_analog(self):
        self.analog_speed = analog.read_channel(self.analog_pin)
        if self.analog_speed < 0:
            self.set_direction(False)
        elif self.analog_speed > 0:
            self.set_direction(True)
            
        self.analog_speed = abs(self.analog_speed)
        # return self.analog_speed
    
    def variable_single_step(self):
        if self.analog_speed > 0:
            GPIO.output(self.step_pin, True)
            time.sleep(self.analog_speed)
            GPIO.output(self.step_pin, False)
            time.sleep(self.analog_speed)
        else:
            return
        if self.current_direction == False:
            self.step_count -= 1
        else:
            self.step_count += 1




    def return_home(self):
        self.enable()
        self.speed = 0.0002
        if self.step_count < 0:
            self.set_direction(True)
        else:
            self.set_direction(False)
        self.step_count = abs(self.step_count)
        for x in range(self.step_count):
            self.single_step()
        self.disable()
        self.step_count = 0

    def enable(self):
        GPIO.output(self.enable_pin, True)
        time.sleep(0.005)        

    def disable(self):
        GPIO.output(self.enable_pin, False)        

    def toggle_enable(self):
        self.enabled = not self.enabled


    def enable_counting(self):
        self.step_count = 0
        self.enable()


    def disable_counting(self):
        print("Total " + self.name +": " + str(self.step_count))
        self.disable()


    def stop_counting(self):
        print("Count: " + str(self.step_count))
        self.disable()

    def find_home(self):
        self.set_direction(self.home_direction)
        self.enable()
        while self.limit():
            self.single_step()
        print("Home Found")
        time.sleep(0.5)
        self.switch_direction()
        for x in range(self.home_step_offset):
            if control.stop():
                break
            else:
                self.single_step()
        # self.count_from_home()
        self.disable()

    def adjust_home(self):
        self.enable()
        while control.stop() == False:
            self.read_analog()
            for x in range(100):
                self.variable_single_step()
        self.disable()

    def reset_from_limit(self):
        away_dir = not self.home_direction
        self.set_direction(away_dir)
        self.enable()
        while self.limit() == False:
            self.single_step()
        for x in range(500):
            self.single_step()
        self.disable()

    def count_from_home(self):
        count = 0
        away_dir = not self.home_direction
        self.set_direction(away_dir)
        while control.stop() == False:
            count += 1
            self.single_step()
        self.disable()
        print("STEPS TAKEN: " + str(count))

    def limit(self):
        limit_status = True
        for l in self.limits:
            if GPIO.input(l) == False:
                limit_status = False
                break
            elif control.stop():
                limit_status = False
                break
            else:
                pass
        return limit_status

    def __clear(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    


