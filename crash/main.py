from kivy.app import app
from kivy.uix.button import button

class TutorialApp(App):
    def build(self):
        return Button(text="HELLO", background_color(0,0,1,1), font_size=150)

if __name__ == "__main__":
    TutorialApp().run()

