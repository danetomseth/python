from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
import time
import stepper
import analog
import limits
from subprocess import call
from kivy.clock import Clock




class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.current_speed = 0.005
        self.init_speed = str(self.current_speed)

    def find_home(self, motor):
        stepper.find_home(motor)

    def adjust_home(self, motor):
        stepper.adjust_home(motor)


    def move(self, motor):
        stepper.move(motor)

    def read_channel(self, motor):
        stepper.read_channel(motor)


    def read_all(self):
        stepper.all_axis_joystick()

    def timing_test(self):
        stepper.timing_test()

    def set_point_A(self):
        call (["gphoto2","--capture-image"])
        stepper.set_A()


    def return_home(self):
        stepper.return_all_home()
        call (["gphoto2","--capture-image"])


    def pano(self):
        stepper.pano_test()

    def pano_tilt(self):
        stepper.pano_tilt()
    

    def decrease_speed(self):
        self.current_speed += 0.0001
        self.ids.speed_label.text = str(self.current_speed)


    def increase_speed(self):
        self.current_speed -= 0.0001
        self.ids.speed_label.text = str(self.current_speed)

    def exit(self):
        stepper.clean()
        App.get_running_app().stop()


class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)

    def read_analog(self):
        stepper.slide_joystick()

    def limit_test(self):
        stepper.limit_test()

    def move_distance(self, motor, distance):
        stepper.move_distance(motor, distance)


    def exit(self):
        stepper.clean()
        App.get_running_app().stop()


class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        self.motors = ["slide", "pan", "tilt"]

    def set_A(self):
        for motor in self.motors:
            self.ids.motor_label.text = "SET: " + motor
            stepper.set_A(motor)
        
        self.ids.motor_label.text = "FINISHED SETTING A"
    def set_B(self):
        stepper.set_B()

    def run_preview(self):
        stepper.run_AB_preview()


    def exit(self):
        stepper.clean()
        App.get_running_app().stop()





class Manager(ScreenManager):
    screen_three = ObjectProperty(None)
    screen_four = ObjectProperty(None)
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    


class TemplateApp(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    TemplateApp().run()