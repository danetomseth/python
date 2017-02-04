from kivy.app import App
# from kivy.lang import Builder
import motor
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.vector import Vector

myNumber = 3

class MyClass(object):
	common = 10
	def __init__(self):
		self.myvar = 3
	def myfunction(self):
		print(self.myvar)

class ScreenOne(Screen):
	def __init__(self, **kwargs):
		super(ScreenOne, self).__init__(**kwargs)
		self.value = 1
		self.localClass = MyClass()
		self.num = myNumber

	def printVars(self):
		motor.move_delay(1, True)

	def cancel_delay(self):
		motor.cancel_delay()

	common = 1





class Manager(ScreenManager):
    screen_one = ObjectProperty(None)
    


class LayoutApp(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    LayoutApp().run()