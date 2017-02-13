#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time


class TimelapseMain(Screen):
    def __init__(self, **kwargs):
        super(TimelapseMain, self).__init__(**kwargs)

    def new_func(self):
        print("Func")


class TimelapseSimple_A(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_A, self).__init__(**kwargs)
        self.timelapse_duration = 60
        self.total_frames = 300

    def modify_duration(self, direction):
        if direction < 0:
            self.timelapse_duration -= 10
        else:
            self.timelapse_duration += 10

        self.ids.timelapse_duration_label.text = "Timelapse Duration \n" + str(self.timelapse_duration) + "min"

    def set_frames(self, direction):
        if direction < 0:
            self.total_frames -= 30
        else:
            self.total_frames += 30

        clip_duration = self.total_frames / 30
        self.ids.total_frames_label.text = "Clip Duration \n" + str(clip_duration) + "s"

        




class TimelapseSimple_B(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_B, self).__init__(**kwargs)

    def set_move_A(self):
        print("move A")


    def set_move_B(self):
        print("move B")

    def start(self):
        print("START")

class TimelapseSimple_C(Screen):
    def __init__(self, **kwargs):
        super(TimelapseSimple_C, self).__init__(**kwargs)






class TimelapseAdvanced_A(Screen):
    def __init__(self, **kwargs):
        super(TimelapseAdvanced_A, self).__init__(**kwargs)


