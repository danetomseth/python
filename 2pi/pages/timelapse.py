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

class TimelapseMain(Screen):
    def __init__(self, **kwargs):
        super(TimelapseMain, self).__init__(**kwargs)

    def new_func(self):
        print("Func")




class TimelapseSimple_A(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_A, self).__init__(**kwargs)
        self.timelapse_duration = stepper.timelapse_duration
        self.total_frames = 300

    def modify_duration(self, direction):
        if direction < 0:
            stepper.timelapse_duration -= 10
        else:
            stepper.timelapse_duration += 10

        self.ids.timelapse_duration_label.text = "Timelapse Duration \n" + str(stepper.timelapse_duration) + "min"

    def set_frames(self, direction):
        if direction < 0:
            self.total_frames -= 30
        else:
            self.total_frames += 30

        clip_duration = self.total_frames / 30
        self.ids.total_frames_label.text = "Clip Duration \n" + str(clip_duration) + "s"

    def picture(self):
        stepper.take_picture

        




class TimelapseSimple_B(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_B, self).__init__(**kwargs)
        self.end_set = False
        

    def set_move_A(self):
        print("SLIDE")
        stepper.set_A('slide')
        print("PAN")
        stepper.set_A('pan')
        print("TILT")
        stepper.set_A('tilt')
        print("FINSHED")

    def set_start(self, other):
        print("move B")
        print("SLIDE")
        stepper.set_B('slide')
        print("PAN")
        stepper.set_B('pan')
        print("TILT")
        stepper.set_B('tilt')
        print("FINSHED")

    def set_end(self):
        if self.end_set == False:
            print("END SET")
            print("SLIDE")
            stepper.set_A('slide')
            print("PAN")
            stepper.set_A('pan')
            print("TILT")
            stepper.set_A('tilt')
            print("FINSHED")
            self.move_button = self.ids.movement_btn
            self.move_button.text = "SET START"
            self.end_set = True
        else:
            print("move B")
            print("SLIDE")
            stepper.set_B('slide')
            print("PAN")
            stepper.set_B('pan')
            print("TILT")
            stepper.set_B('tilt')
            print("FINSHED")
            self.move_button.text = "FINISHED"


    def set_move_B(self):
        print("move B")
        print("SLIDE")
        stepper.set_B('slide')
        print("PAN")
        stepper.set_B('pan')
        print("TILT")
        stepper.set_B('tilt')
        print("FINSHED")

    def run_preview(self):
        stepper.run_AB()

    def start(self, root_widget):
        print("START")
        print(root_widget)
        root_widget.manager.curent = 'timelapse_simpleC'

class TimelapseSimple_C(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_C, self).__init__(**kwargs)
        self.check_interval = 0.1

    def preview_movement(self):
        stepper.run_AB()

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


