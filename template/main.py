from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
import time
import stepper



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
        self.current_speed += 0.00005
        self.ids.speed_label.text = str(self.current_speed)


    def increase_speed(self):
        self.current_speed -= 0.00005
        self.ids.speed_label.text = str(self.current_speed)

    def exit(self):
        stepper.clean()
        App.get_running_app().stop()





class Manager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    


class TemplateApp(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    TemplateApp().run()