from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
# Builder.load_string("""
# <MenuScreen>:
#     name: 'menu'
#     BoxLayout:
#         Button:
#             text: 'Goto settings'
#             on_press: root.manager.current = 'settings'
#         Button:
#             text: 'Quit'

# <SettingsScreen>:
#     name: 'settings'
#     BoxLayout:
#         Button:
#             text: 'My settings button'
#         Button:
#             text: 'Go to New item'
#             on_press: root.manager.current = 'newitem'
# <NewItem>:
#     name: 'newitem'
#     BoxLayout:
#         Button:
#             text: 'new button'
#         Button:
#             text: 'Back to menu'
#             on_press: root.manager.current = 'settings'
# """)

# Declare both screens

class MenuScreen(Screen):
    pass

class NewItem(Screen):
    pass

class SettingsScreen(Screen):
    pass

class Manager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)

# class MainWindow()
#     pass
   




# Create the screen manager
# sm = ScreenManager()
# sm = WindowManager()
# sm.add_widget(MenuScreen())
# sm.add_widget(SettingsScreen())
# sm.add_widget(NewItem())

class TestApp(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    TestApp().run()