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
import stepper


class SettingsScreen(Screen):
    step_mode_tab = ObjectProperty(None)
    control_tab = ObjectProperty(None)
    camera_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

class StepMode(BoxLayout):
    page_title = StringProperty('STEPPER SETTINGS')
    def __init__(self, **kwargs):
        super(StepMode, self).__init__(**kwargs)


    def set_slide(self, mode):
        stepper.slide_microstep(mode)

    def set_pan(self, mode):
        stepper.pan_microstep(mode)


class ControlTab(BoxLayout):
    page_title = StringProperty('CONTROL SETTINGS')
    def __init__(self, **kwargs):
        super(ControlTab, self).__init__(**kwargs)

    def set_control_joystick(self):
        stepper.set_control_joystick()

    def set_control_ps3(self):
        stepper.set_control_ps3()


    

    def test(self):
        print("TESTING")
        stepper.test_control_mode()

    def baseline(self):
        stepper.baseline()
        

class CameraTab(BoxLayout):
    page_title = StringProperty('CAMERA SETTINGS')
    def __init__(self, **kwargs):
        super(CameraTab, self).__init__(**kwargs)
        
    def set_shutter_usb(self):
        camera.set_control_usb()


    def set_shutter_remote(self):
        camera.set_control_remote()