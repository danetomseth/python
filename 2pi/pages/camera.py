#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time
import stepper

from stepper import camera


class CameraScreen(Screen):
    flex_item = ObjectProperty(None)
    camera_widget = ObjectProperty(None)
    parent_box = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.shutter_text = self.get_shutter_text()
    
    def picture(self):
        start = time.time()
        camera.test_capture()
        end = time.time() - start
        print("TIME: " + str(end))



    def quick_picture(self):
        start = time.time()
        camera.quick_picture()
        end = time.time() - start
        print("TIME: " + str(end))

    def function_C(self):
        print("RUNNING C")

    def function_D(self):
        print("RUNNING D")


    def remove(self):
        print("ITEM")
        print(self.flex_item)
        print(self.parent_box)
        print(self.camera_widget)
        self.parent_box.remove_widget(self.flex_item)


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


