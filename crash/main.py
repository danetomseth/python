from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty

from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color

from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp


class PageTitle(BoxLayout):
    title = StringProperty('')

class ParentBox(BoxLayout):
    updated_text = StringProperty("input")
    def __init__(self, **kwargs):
        super(ParentBox, self).__init__(**kwargs)

    def change_text(self, *args):
        self.updated_text = self.ids.my_input.text
        # print("Updated: " + self.updated_text)

    def clear_text(self):
        self.ids.my_input.text = ""
        self.updated_text = ""


class ImageBox(BoxLayout):
    page_title = StringProperty("TITLEEE")
    def __init__(self, **kwargs):
        super(ImageBox, self).__init__(**kwargs)

    def action(self):
        self.page_title = "HELLO"



class TutorialApp(App):
    def build(self):
        return ImageBox()

if __name__ == "__main__":
    TutorialApp().run()

