from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import RPi.GPIO as GPIO ## Import GPIO library
import time



class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.limit_left = 23
        self.limit_right = 24
        GPIO.setmode(GPIO.BCM) ## Use board pin numbering
        GPIO.setup(self.limit_left, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out
        GPIO.setup(self.limit_right, GPIO.IN, pull_up_down=GPIO.PUD_UP) ##setup gpio as out

        self.limit_status = "No Input"
        

    def cancelReading(self):
    	self.ids['limit_label'].text = "Canceled"
    	self.program_interval.cancel()

    def readLimits(self, dt):
    	self.left_end = GPIO.input(self.limit_left)
    	self.right_end = GPIO.input(self.limit_right)
    	if self.left_end == False:
    	    self.ids['limit_label'].text = "Left Limit"
    	    time.sleep(0.2)

    	if self.right_end == False:
    		self.ids['limit_label'].text = "Right Limit"
    		time.sleep(0.2)

    def checkButtons(self):
    	
    	self.program_interval = Clock.schedule_interval(self.readLimits, 0.1)

class Manager(ScreenManager):
    screen_one = ObjectProperty(None)
    


class ButtonApp(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    ButtonApp().run()