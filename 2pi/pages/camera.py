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
import gphoto2 as gp
import logging

# gp.error_severity[gp.GP_ERROR] = logging.WARNING

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

class CameraControl(Screen):
    page_title = StringProperty('CAMERA CONTROL')
    def __init__(self, **kwargs):
        super(CameraControl, self).__init__(**kwargs)
        self.context = gp.Context()
        self.camera = gp.Camera()
        self.camera.init(self.context)
        self.camera_options = self.camera.get_config(self.context)

    def camera_context(self):
        # text = camera.get_summary(context)
        text = self.camera.get_abilities()
        print('Summary')
        print('=======')
        print(str(text))

    def config(self):
        options = self.camera.get_config(self.context)
        print(options)
        child_count = options.count_children()
        if child_count < 1:
            print('no children')
            return
        for n in range(child_count):
            child = options.get_child(n)
            label = '{} ({})'.format(child.get_label(), child.get_name())
            print(label)
            self.list_children(child)
            print("-----------")

    def list_children(self, child):
        count = child.count_children()
        if count < 1:
            # print("-----")
            return
        else:
            for n in range(count):
                option = child.get_child(n)
                label = '{} ({})'.format(option.get_label(), option.get_name())
                print(label)
                print(option.get_value())
                if option.get_name() == 'iso':
                    choices = option.count_choices()
                    for x in range(choices):
                        print(option.get_choice(x))
                    option.set_value('100')
                        
                    print("*******************")
                # self.list_children(option)

    def capture(self):
        self.camera.trigger_capture(self.context)


    def run_timelapse(self):
        for x in range(1900):
            if x % 30 == 0:
                self.change_shutter()
                time.sleep(1)
            self.capture()
            time.sleep(6)
            print(str(x))

    def change_shutter(self):
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
        setting = gp.check_result(
        gp.gp_widget_get_child_by_name(config, 'shutterspeed'))
        current = setting.get_value()
        total_values = setting.count_choices()
        
        for x in range(total_values):
            value = gp.check_result(gp.gp_widget_get_choice(setting, x))
            if value == current:
                current_index = x -1
                value = gp.check_result(gp.gp_widget_get_choice(setting, current_index))
                gp.check_result(gp.gp_widget_set_value(setting, value))
                gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))
                break

    def get_item(self):
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
        setting = gp.check_result(
        gp.gp_widget_get_child_by_name(config, 'shutterspeed'))
        current = setting.get_value()
        print(current)
        total_values = setting.count_choices()
        print(total_values)
        
        for x in range(total_values):
            value = gp.check_result(gp.gp_widget_get_choice(setting, x))
            if value == current:
                print("Found")
                print(x)
                print(value)
                current_index = x -1
                value = gp.check_result(gp.gp_widget_get_choice(setting, current_index))
                gp.check_result(gp.gp_widget_set_value(setting, value))
                gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))
                self.capture()
                break
        # time.sleep(2)
        # for x in range(5):
        #     current_index -= 1
        #     value = gp.check_result(gp.gp_widget_get_choice(setting, current_index))
        #     gp.check_result(gp.gp_widget_set_value(setting, value))
        #     gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))
        #     time.sleep(1)
        #     self.capture()
        #     print(value)
        #     time.sleep(1)
        #     if x > 5:
        #         break
        
                




