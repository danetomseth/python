#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.dropdown import DropDown
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
    main_widget = ObjectProperty(None)
    movement_btn = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(TimelapseSimple_B, self).__init__(**kwargs)
        self.end_set = False
        
    def reset_timelapse(self):
        self.end_set = False
        self.ids.movement_btn.text = "SET END"
        stepper.reset_timelapse()

    def set_move_points(self):
        if self.end_set == False:
            stepper.joystick_set_end()
            self.move_button = self.ids.movement_btn
            self.move_button.text = "SET START"
            self.end_set = True
        else:
            stepper.joystick_set_start()
            self.end_set = False
            self.main_widget.remove_widget(self.movement_btn)
            self.main_widget.add_widget(Label(text="MOVEMENT SET", font_size="40sp"))


class TimelapseSimple_C(Screen):
    progress_widget = ObjectProperty(None)
    progress_label = ObjectProperty(None)
    preview_btn = ObjectProperty(None)
    progress = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(TimelapseSimple_C, self).__init__(**kwargs)
        self.check_interval = 0.5
        self.progress = 0
        self.previewed = False


    def preview_movement(self):
        if self.previewed:
            stepper.reset_position()
            self.preview_btn.text = "PREVIEW"
            self.previewed = False
        else:
            stepper.timelapse_preview()
            self.preview_btn.text = "RESET"


        

    def program_timelapse(self):
        self.total_steps = camera.total_pictures
        self.steps_taken = 1
        self.ids.total_pictures.text = str(camera.picture_count)
        stepper.program_timelapse()
        camera.initialize_camera()

    def run_program(self, dt):
        stepper.timelapse_step()
        self.calculate_progress()
        if stepper.timelapse_active == False:
            print("canceled")
            self.program_interval.cancel()

    def finish_program(self):
        self.progress_widget.remove_widget(self.timelapse_progress)
        self.progress_widget.remove_widget(self.progress_label)
        self.progress_widget.add_widget(Label(text="FINISHED", font_size="20sp"))
        self.ids.total_pictures.text = "FINISHED"

    def calculate_progress(self):
        # self.ids.timelapse_progress.value = int((float(camera.picture_count) / float(camera.total_pictures)) * 100)
        self.progress = int((float(camera.picture_count) / float(camera.total_pictures)) * 100)
        self.ids.total_pictures.text = str(camera.picture_count)
        if self.progress >= 100:
            print("CANCEL FROM PROGRESS")
            self.finish_program()
            self.program_interval.cancel()


    def initiate_program(self):
        self.program_timelapse()
        self.program_interval = Clock.schedule_interval(self.run_program, camera.timelapse_interval)

    def cancel_program(self):
        self.program_interval.cancel()






class TimelapseAdvanced_A(Screen):
    def __init__(self, **kwargs):
        super(TimelapseAdvanced_A, self).__init__(**kwargs)


