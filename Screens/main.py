from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
import sys
import time



 





class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def next_screen(self):
        new_screen = self.manager.get_screen('alt')
        self.manager.current = 'alt'
        print(new_screen)
        print(self.manager.screens)



class AltScreen(Screen):
    def __init__(self, **kwargs):
        super(AltScreen, self).__init__(**kwargs)
    def next_screen(self):
        new_screen = self.manager.get_screen('home')
        self.manager.current = 'home'
        print(new_screen)
        print(self.manager.screen_names)


class Manager(ScreenManager):
    home_screen = ObjectProperty(None)
    alt_screen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.transition = WipeTransition()




class TemplateApp(App):
    
    def build(self):
        return Manager()

    def exit(self):
        App.get_running_app().stop()


if __name__ == '__main__':
    TemplateApp().run()