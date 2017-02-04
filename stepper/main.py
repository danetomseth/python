from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import time


class MainWindow(GridLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def step_forward(self):
    	print("forward")

    def step_reverse(self):
    	print("reverse")


class StepperApp(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    StepperApp().run()