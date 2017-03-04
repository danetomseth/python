#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time



# from cameraClass import camera
from cameraClass import camera


class CameraScreen(Screen):
    camera_widget = ObjectProperty(None)
    page_title = StringProperty('CAMERA')
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.shutter_text = self.get_shutter_text()
        self.pic_count = 0
        self.startTime = time.time()
    
    def picture(self):
        camera.capture_image()

    def burst_trigger(self, dt):
        self.startTime = time.time()
        if self.pic_count < 5:
            camera.trigger()
            self.pic_count += 1
            print(str(self.pic_count))
            endTime = time.time() - self.startTime
            print(str(endTime))
        else:
            print("FINSIHED")
            self.program_interval.cancel()



    def quick_picture(self):
        start = time.time()
        camera.trigger()
        end = time.time() - start
        print("TIME: " + str(end))

    def initialize_camera(self):
        start = time.time()
        camera.initialize()
        end = time.time() - start
        print("TIME: " + str(end))




    def burst(self):
        self.program_interval = Clock.schedule_interval(self.burst_trigger, 0.25)



    def bulb(self):
        for x in range(10):
            start = time.time()
            camera.bulb_picture()
            end = time.time() - start
            print("TIME: " + str(end))
            self.modify_shutter(1)

    def modify_shutter(self, direction):
        camera.modify_bulb_time(direction)

        self.ids.shutter.text = self.get_shutter_text()

    def get_shutter_text(self):
        return "Shutter Speed: " + str(camera.shutter_time) + 's'

class PanoScreen(Screen):
    page_title = StringProperty('PANORAMA')
    pan_degrees = NumericProperty(45)
    def __init__(self, **kwargs):
        super(PanoScreen, self).__init__(**kwargs)
        self.direction = "RIGHT"

    def set_degrees(self, direction):
        if direction < 0:
            if self.pan_degrees > 5:
                self.pan_degrees -= 5
        else:
            if self.pan_degrees < 270:
                self.pan_degrees += 5

    def set_direction(self, direction):
        if direction:
            self.direction = "RIGHT"
        else:
            self.direction = "LEFT"



class FocusScreen(Screen):
    page_title = StringProperty('FOCUS STACK')
    bulb_time = NumericProperty(0.5)
    def __init__(self, **kwargs):
        super(FocusScreen, self).__init__(**kwargs)

    def set_shutter(self, direction):
        if direction < 0:
            if self.bulb_time > 0:
                self.bulb_time = self.bulb_time * 0.9
        else:
            self.bulb_time = self.bulb_time * 1.1

    def run_bulb(self):
        for x in range(5):
            camera.bulb(self.bulb_time)

    def test_bulb(self):
        camera.bulb(self.bulb_time)




