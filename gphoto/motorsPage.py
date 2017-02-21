from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time



class StepperMotor(BoxLayout):
    def __init__(self, *args, **kwargs):
        print(args)
        super(StepperMotor, self).__init__(**kwargs)
        if len(args) > 0:
            self.name = args[0]
            self.steps = args[1]

        # self.name = name

    def setName(self, name):
        print("setting")
        self.ids.motor_name.text = self.name

    def action(self):
        print(self.name)
        self.ids.motor_name.text = self.name

    def exit_app(self):
        
        App.get_running_app().stop()





class SlideTab(BoxLayout):
    def __init__(self, **kwargs):
        super(SlideTab, self).__init__(**kwargs)
        self.title = "SLIDE"
        self.set_speed = 1000
        self.steps_programmed = 64000
        self.set_direction = 'LEFT'

        self._set_speed = 'Speed: ' + str(self.set_speed)
        self._steps_programmed = 'Steps: ' + str(self.steps_programmed)
        self._set_direction = 'Direction: ' + self.set_direction
    
    def control(self):
        print("Joystick")


    def find_home(self):
        print("HOMEEEE")

    def ramp_test(self):
        print("Ramp")

    def adjust_speed(self, dir_mod):
        if dir_mod < 0:
            self.set_speed -= 100
        else:
            self.set_speed += 100 
        self.update_labels()


    def update_labels(self):
        self.ids.set_speed_label.text = 'Speed: ' + str(self.set_speed)
        self.ids.steps_programmed_label.text = 'Steps: ' + str(self.steps_programmed)
        self.ids.set_direction_label.text = 'Direction: ' + self.set_direction 

    def exit_app(self):
        
        App.get_running_app().stop()



class PanTab(BoxLayout):
    def __init__(self, **kwargs):
        super(PanTab, self).__init__(**kwargs)
        self.title = "PAN"
        self.set_speed = 1000
        self.steps_programmed = 64000
        self.set_direction = 'LEFT'

        self._set_speed = 'Speed: ' + str(self.set_speed)
        self._steps_programmed = 'Steps: ' + str(self.steps_programmed)
        self._set_direction = 'Direction: ' + self.set_direction
    
    def control(self):
        print("Joystick")
        

    def find_home(self):
        print("HOMEEEE")

    def ramp_test(self):
        print("Ramp")

    def adjust_speed(self, dir_mod):
        if dir_mod < 0:
            self.set_speed -= 100
        else:
            self.set_speed += 100 
        self.update_labels()


    def update_labels(self):
        self.ids.set_speed_label.text = 'Speed: ' + str(self.set_speed)
        self.ids.steps_programmed_label.text = 'Steps: ' + str(self.steps_programmed)
        self.ids.set_direction_label.text = 'Direction: ' + self.set_direction 

    def exit_app(self):
        
        App.get_running_app().stop()

class TiltTab(BoxLayout):
    def __init__(self, **kwargs):
        super(TiltTab, self).__init__(**kwargs)
        self.title = "TILT"
        self.set_speed = 1000
        self.steps_programmed = 64000
        self.set_direction = 'LEFT'

        self._set_speed = 'Speed: ' + str(self.set_speed)
        self._steps_programmed = 'Steps: ' + str(self.steps_programmed)
        self._set_direction = 'Direction: ' + self.set_direction
    
    def control(self):
        print("Joystick")
        

    def find_home(self):
        print("HOMEEEE")

    def ramp_test(self):
        print("Ramp")

    def adjust_speed(self, dir_mod):
        if dir_mod < 0:
            self.set_speed -= 100
        else:
            self.set_speed += 100 
        self.update_labels()


    def update_labels(self):
        self.ids.set_speed_label.text = 'Speed: ' + str(self.set_speed)
        self.ids.steps_programmed_label.text = 'Steps: ' + str(self.steps_programmed)
        self.ids.set_direction_label.text = 'Direction: ' + self.set_direction 

    def exit_app(self):
        
        App.get_running_app().stop()
