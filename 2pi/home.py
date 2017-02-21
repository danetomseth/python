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
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import sys
import time

# kivy files
import timelapse
import control
import video
# Control Files
import stepper
import camera

sys.path.append('./pages')
sys.path.append('./controls')

class E(ExceptionHandler):
    def handle_exception(self, inst):
        print("********EXCEPTION********")
        Logger.exception('CAUGHT EXCEPTION')
        stepper.clean()
        App.get_running_app().stop()
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


    def test_func(self):
        temp.temp_func()



class ControlScreen(Screen):
    slide_tab = ObjectProperty(None)
    pan_tab = ObjectProperty(None)
    tilt_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs)