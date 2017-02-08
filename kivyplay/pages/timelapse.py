#!/usr/bin/env python

from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time


class TimelapseScreen(Screen):
    def __init__(self, **kwargs):
        super(TimelapseScreen, self).__init__(**kwargs)

    def new_func(self):
        print("Func")

