#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time

from datetime import datetime
from datetime import timedelta
import subprocess


from wrappers import GPhoto
from wrappers import Identify
from wrappers import NetworkInfo

CONFIGS = [("1/8000", 200),
           ("1/6400", 200),
           ("1/5000", 200),
           ("1/4000", 200),
           ("1/3200", 200),
           ("1/2500", 200),
           ("1/2000", 200),
           ("1/1600", 200),
           ("1/1250", 200),
           ("1/1000", 200),
           ("1/800", 200),
           ("1/640", 200),
           ("1/500", 200),
           ("1/400", 200),
           ("1/320", 200),
           ("1/250", 200),
           ("1/200", 200),
           ("1/160", 200),
           ("1/125", 200),
           ("1/100", 200),
           ("1/80", 200),
           ("1/60", 200),
           ("1/50", 200),
           ("1/40", 200),
           ("1/30", 200),
           ("1/25", 200),
           ("1/20", 200),
           ("1/15", 200),
           ("1/13", 200),
           ("1/10", 200),
           ("1/8", 200),
           ("1/6", 200),
           ("1/5", 200),
           ("1/4", 200),
           ("0.3", 200),
           ("0.4", 200),
           ("0.5", 200),
           ("0.6", 200),
           ("0.8", 200),
           ("1", 200),
           ("1.3", 200),
           ("1.6", 200),
           ("2", 200),
           ("2.5", 200),
           ("3.2", 200),
           ("4", 200),
           ("5", 200),
           ("6", 200),
           ("8", 200),
           ("10", 200),
           ("13", 200),
           ("15", 200),
           ("20", 200),
           ("25", 200),
           ("30", 200),
           ("30", 1600)]




camera = GPhoto(subprocess)



class PhotoScreen(Screen):
    def __init__(self, **kwargs):
        super(PhotoScreen, self).__init__(**kwargs)
        self.shutter_index = 15
        self.shutter_time = 0.03
        
        
    





    def test_configs(self):
        pass
        # for config in CONFIGS:
        #     print(config[0])
        #     camera.set_shutter_speed(secs=config[0])
        #     camera.set_iso(iso=str(config[1]))
        #     time.sleep(1)


    def connect_camera(self):
        camera.capture_image()



    def get_config(self):
        camera.get_shutter_speeds()
        camera.get_isos()


    def set_shutter(self):
        current = CONFIGS[self.shutter_index]

        camera.set_shutter_speed(secs=current[0])
        print("SHUTTER: " + current[0])
        self.shutter_index -= 1

    def increase_bulb(self):
        self.shutter_time += 0.025
        print("SHUTTER: " + str(self.shutter_time))


    def set_iso(self):
        print("ISO")


    def trigger(self):
        print("START")
        camera.trigger()
        print("DONE")


    def capture_image(self):
        print("START")
        camera.capture_image()
        print("DONE")

    def bulb_trigger(self):
        camera.bulb_trigger(self.shutter_time)


