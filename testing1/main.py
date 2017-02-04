from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
import time
import stepper
import analog
import limits
from kivy.clock import Clock



stepper.gpio_setup()

class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.current_speed = 0.005
        self.init_speed = str(self.current_speed)


    def move_A(self):
        stepper.run_A(self.current_speed)

    def move_B(self):
        stepper.run_B(self.current_speed)

    def move_C(self):
        stepper.run_C(self.current_speed)

    def enable_all(self):
        stepper.enable_all()

    def disable_all(self):
        stepper.disable_all()
    

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
        analog.read_values()


    def exit(self):
        stepper.clean()
        App.get_running_app().stop()


class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)

    def read_analog(self):
        analog.read_values()

    def run_motor(self, motor):
        if motor == "slide":
            stepper.test_slide()
        elif motor == "pan":
            stepper.test_pan()
        elif motor == "tilt":
            stepper.test_tilt()
        else:
            print("Invalid Motor")


    def update_labels(self, dt):
        label_arr = analog.get_values()
        if stepper.stop():
            print("Cancelled")
            self.ids.pan_label.text = "PAN: \n Waiting..."
            self.ids.tilt_label.text = "TILT: \n Waiting..."
            self.ids.slide_label.text = "SLIDE: \n Waiting..."
            self.program_interval.cancel()
        else:
            self.ids.pan_label.text = "PAN: \n" + str(label_arr[0])
            self.ids.tilt_label.text = "TILT: \n" + str(label_arr[1])
            self.ids.slide_label.text = "SLIDE: \n" + str(label_arr[2])


    def watch_labels(self):
        self.program_interval = Clock.schedule_interval(self.update_labels, 0.5)


    def exit(self):
        stepper.clean()
        App.get_running_app().stop()


class ScreenFour(Screen):
    def __init__(self, **kwargs):
        super(ScreenFour, self).__init__(**kwargs)
        self.set_speed = 0.0005

    def run_limit_test(self):
        stepper.run_limit_test(self.set_speed)

    def read_limits(self):
        limits.read_all()

    def decrease_speed(self):
        self.set_speed -= 0.0001
        self.ids.current_speed.text = str(self.set_speed)


    def update_labels(self, dt):
        label_arr = analog.get_values()
        if stepper.stop():
            self.program_interval.cancel()
        else:
            pass
            # self.ids.pan_label.text = "PAN: \n" + str(label_arr[0])
            # self.ids.tilt_label.text = "TILT: \n" + str(label_arr[1])
            # self.ids.slide_label.text = "SLIDE: \n" + str(label_arr[2])


    def watch_labels(self):
        self.program_interval = Clock.schedule_interval(self.update_labels, 0.5)


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