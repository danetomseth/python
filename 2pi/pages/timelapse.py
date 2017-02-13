#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
import time
import sys

sys.path.append('./controls')
import stepper

from stepper import camera

class TimelapseMain(Screen):
    def __init__(self, **kwargs):
        super(TimelapseMain, self).__init__(**kwargs)

    def new_func(self):
        print("Func")




class TimelapseSimple_A(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_A, self).__init__(**kwargs)
        self.timelapse_duration = self.get_duration_text()
        self.timelapse_interval = self.get_interval_text()
        self.clip_duration = self.get_clip_duration_text()

    def set_duration(self, direction):
        camera.set_duration(direction)

        self.ids.timelapse_duration_label.text = self.get_duration_text()
        self.ids.clip_duration_label.text = self.get_clip_duration_text()

    def set_interval(self, direction):
        camera.set_interval(direction)

        self.ids.timelapse_interval_label.text = self.get_interval_text()
        self.ids.clip_duration_label.text = self.get_clip_duration_text()


    def get_duration_text(self):
        return "Timelapse Duration: " + str(camera.timelapse_duration) + "min"

    def get_interval_text(self):
        return "Interval: " + str(camera.timelapse_interval) + "s"

    def get_clip_duration_text(self):
        return "Clip Duration: " + str(camera.clip_duration) + "s"

        




class TimelapseSimple_B(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_B, self).__init__(**kwargs)
        self.end_set = False
        


    def set_move_points(self):
        if self.end_set == False:
            stepper.joystick_set_end()
            self.move_button = self.ids.movement_btn
            self.move_button.text = "SET START"
            self.end_set = True
        else:
            stepper.joystick_set_start()
            self.move_button.text = "FINISHED"
            self.end_set = False


class TimelapseSimple_C(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_C, self).__init__(**kwargs)
        self.check_interval = 0.1

    def preview_movement(self):
        stepper.run_timelapse_preview()

    def run_program(self, dt):
        self.ids.timelapse_progress.value += 1
        print('updating: ' + str(self.ids.timelapse_progress.value))
        if self.ids.timelapse_progress.value == 100:
            print("canceled")
            self.program_interval.cancel()


    def initiate_program(self):
        self.program_interval = Clock.schedule_interval(self.run_program, self.check_interval)

    def cancel_program(self):
        self.program_interval.cancel()






class TimelapseAdvanced_A(Screen):
    def __init__(self, **kwargs):
        super(TimelapseAdvanced_A, self).__init__(**kwargs)


