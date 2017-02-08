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
# import stepperControl as stepper
import controlTest as stepper
import motorsPage
# import temp

 

# class MotorPage(Accordion):
#     slide_tab = ObjectProperty(None)
#     pan_tab = ObjectProperty(None)
#     tilt_tab = ObjectProperty(None)

class MotorsScreen(Screen):

    slide_tab = ObjectProperty(None)
    pan_tab = ObjectProperty(None)
    tilt_tab = ObjectProperty(None)
    new_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MotorsScreen, self).__init__(**kwargs)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def display(self, val):
        print("Pressed: " + val)

newMotor = StepperMotor('slide', 62000)

class Manager(ScreenManager):
    home_screen = ObjectProperty(None)
    motors_screen = ObjectProperty(None)


class PilapseApp(App):
    
    def build(self):
        return Manager()


if __name__ == '__main__':
    PilapseApp().run()