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



    def read_txd(self):
        stepper.shutter()

    def test(self):
        stepper.test()

    def read_rxd(self):
        stepper.read_rxd()

    def read_stop(self):
        stepper.read_stop()

    
    

    

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