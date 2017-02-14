from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.base import ExceptionHandler
from kivy.base import ExceptionManager
from kivy.logger import Logger

from kivy.uix.boxlayout import BoxLayout
import sys
import time

sys.path.append('./pages')
sys.path.append('./controls')


# kivy files
import timelapse
import control
import video
import camera

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

    camera_screen = ObjectProperty(None)

    # Settings
    control_screen = ObjectProperty(None)

class E(ExceptionHandler):
    def handle_exception(self, inst):
        print("********EXCEPTION********")
        Logger.exception('CAUGHT EXCEPTION')
        stepper.clean()
        App.get_running_app().stop()
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())


class KvmainApp(App):
    
    def build(self):
        self.manager = Manager()
        return self.manager

    def exit(self):
        stepper.clean()
        App.get_running_app().stop()

    def find_home(self, motor):
        stepper.find_home(motor)

    def find_home_all(self):
        stepper.find_home_all()

    def diff_speed(self):
        stepper.home_speed_offset()


    



if __name__ == '__main__':
    KvmainApp().run()