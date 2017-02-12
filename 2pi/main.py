from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
import sys
import time

sys.path.append('./pages')
sys.path.append('./controls')


# kivy files
import timelapse
import control
import video

# Control Files
import stepper



class ControlScreen(Screen):
    slide_tab = ObjectProperty(None)
    pan_tab = ObjectProperty(None)
    tilt_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


    def test_func(self):
        temp.temp_func()


class Manager(ScreenManager):
    home_screen = ObjectProperty(None)
    
    # Live motion
    video_screen = ObjectProperty(None)


    # Timelapse
    timelapse_main = ObjectProperty(None)
    timelapse_simpleA = ObjectProperty(None)
    timelapse_simpleB = ObjectProperty(None)
    timelapse_simpleC = ObjectProperty(None)

    timelapse_advancedA = ObjectProperty(None)

    # Settings
    control_screen = ObjectProperty(None)




class KvmainApp(App):
    
    def build(self):
        self.manager = Manager()
        return self.manager

    def exit(self):
        App.get_running_app().stop()
        stepper.clean()

    def find_home(self, motor):
        stepper.find_home(motor)

    def find_home_all(self):
        stepper.find_home_all()

    def diff_speed(self):
        stepper.home_speed_offset()



if __name__ == '__main__':
    KvmainApp().run()