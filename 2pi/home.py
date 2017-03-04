#!/bin/env python
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
from kivy.core.window import Window
import sys

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


class PageTitle(BoxLayout):
    title = StringProperty('title')

class E(ExceptionHandler):
    def handle_exception(self, inst):
        print("********EXCEPTION********")
        Logger.exception('CAUGHT EXCEPTION')
        stepper.clean()
        App.get_running_app().stop()
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())


class HomeScreen(Screen):
    page_title = StringProperty('PiLapse')
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        # self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)


    def wait_for_key(self):
        print("FINISHED")
        stepper.check_for_key()

    # def _keyboard_closed(self):
    #     print("CLOSED")
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None

    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     if keycode[1] == 'w':
    #         print("EXIT")
    #     else:
    #         print(keycode[1])
    #     return True
            

   



class ControlScreen(Screen):
    slide_tab = ObjectProperty(None)
    pan_tab = ObjectProperty(None)
    tilt_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs)