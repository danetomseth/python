from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.adapters.models import SelectableDataItem
from kivy.graphics import Color, Ellipse, Line
from subprocess import call
import stepper
import time



# Constants
LEFT = False
RIGHT = True

HOME = True
AWAY = False

UP = True
DOWN = False


program_mode = "timelapse"

stepper.gpio_setup()


class ProgramSettings(object):
    def __init__(self):
        self.interval = 3
        self.event_duration = 30
        self.totalPictures = 300
        self.current_picture_count = 0

    def calculate_total_pictures(self):
        secondCount = self.event_duration * 60
        self.totalPictures = int(round(secondCount / self.interval))
        print("Pictures: " + str(self.totalPictures))


class Manager(ScreenManager):
    main_page = ObjectProperty(None)
    admin_screen = ObjectProperty(None)
    initialize_screen = ObjectProperty(None)
    motor_page = ObjectProperty(None)
    slide_page = ObjectProperty(None)
    pan_page = ObjectProperty(None)
    tilt_page = ObjectProperty(None)
    user_page = ObjectProperty(None)
    video_page_a = ObjectProperty(None)
    timelapse_page_a = ObjectProperty(None)
    timelapse_page_b = ObjectProperty(None)
    timelapse_page_c = ObjectProperty(None)





class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def endProgram(self):
        stepper.cleanup()
        App.get_running_app().stop()



class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        global settings
        settings = ProgramSettings()

    def exit(self): 
        stepper.cleanup()  

    def check_inputs(self):
        print("CHECKING")
        stepper.check_inputs()     
    
    def endProgram(self):
        stepper.cleanup()
        App.get_running_app().stop()
        

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)

    def endProgram(self):
        stepper.cleanup()
        App.get_running_app().stop()


class UserPage(Screen):
    def __init__(self, **kwargs):
        super(UserPage, self).__init__(**kwargs)

    def exit(self): 
        stepper.cleanup()       
    
    def endProgram(self):
        stepper.cleanup()
        App.get_running_app().stop()

class VideoA(Screen):
    def __init__(self, **kwargs):
        super(VideoA, self).__init__(**kwargs)

    def endProgram(self):
        stepper.cleanup()
        App.get_running_app().stop()

    def test_run(self):
        stepper.test_video_run()

    def test_start(self):
        stepper.test_start()

    def test_end(self):
        stepper.test_end()

class TimelapseA(Screen):
    def __init__(self, **kwargs):
        super(TimelapseA, self).__init__(**kwargs)

    def change_slide_dir(self, direction):
        stepper.change_slide_direction(direction)

    def change_pan_dir(self, direction):
        stepper.change_pan_direction(direction)

    def change_tilt_dir(self, direction):
        stepper.change_tilt_direction(direction)


    def reset_to_home(self):
        stepper.timelapse_home()

    def jog_slide(self):
        stepper.jog_slide()

    def jog_pan(self):
        stepper.jog_pan()

    def jog_tilt(self):
        stepper.jog_tilt()

    

    def preview_movement(self):
        stepper.timelapse_reset_start()
        stepper.slide_programed_test()
        stepper.pan_programed_test()
        stepper.tilt_programed_test()


    def endProgram(self):
        stepper.cleanup()
        App.get_running_app().stop()

class TimelapseB(Screen):
    def __init__(self, **kwargs):
        super(TimelapseB, self).__init__(**kwargs)
        self.event_duration = "Event: " + str(settings.event_duration) + 'min'
        self.default_duration = settings.event_duration


    def set_interval(self, intTime):
        global settings
        settings.interval = intTime
        settings.calculate_total_pictures()

    def change_event_duration(self):
        global settings
        settings.event_duration = self.ids.duration_slider.value
        self.ids.event_duration_label.text = "Event: " + str(settings.event_duration) + 'min'
        settings.calculate_total_pictures()

    def set_slide_start(self):
        stepper.set_slide_start()

    def set_pan_start(self):
        stepper.set_pan_start()

    def set_tilt_start(self):
        stepper.set_tilt_start()



class TimelapseC(Screen):
    def __init__(self, **kwargs):
        super(TimelapseC, self).__init__(**kwargs)

    
    def test_picture(self):
        call (["gphoto2","--capture-image"])  

    def takePicture(self):
        global settings
        settings.current_picture_count += 1
        call (["gphoto2","--capture-image"])  

    def run_program(self, dt):
        if stepper.timelapse_step():
            self.program_interval.cancel()
        time.sleep(1)
        self.takePicture()

        if settings.current_picture_count > settings.totalPictures:
            self.program_interval.cancel()

    def preview_movement(self):
        stepper.calculate_ratios()
        print("RESETING")
        time.sleep(3)
        stepper.preview_timelapse_fluid()
        # stepper.reset_timelapse_start()


    def start_program(self):
        stepper.calculate_steps_cycle(settings.totalPictures)
        self.program_interval = Clock.schedule_interval(self.run_program, settings.interval)

    def stop_program(self):
        self.program_interval.cancel()



class InitializeScreen(Screen):
    def __init__(self, **kwargs):
        super(InitializeScreen, self).__init__(**kwargs)
        self.label = "Hello"

    def set_pan_dir(self, direction):
        if direction == 'left':
            print("pan left")
        else:
            print('pan right')

    def set_slide_dir(self, direction):
        if direction == 'home':
            print('slide home')
        else:
            print("slide away")

    def set_tilt_dir(self, direction):
        if direction == 'up':
            print('tilt up')
        else:
            print(direction)

    def toggle_motor(self, motor):
        if motor == 'slide':
            if stepper.toggle_motor('slide'):
                self.ids.slide_motor.text = "SLIDE ON"
            else:
                self.ids.slide_motor.text = "SLIDE OFF"
        elif motor == 'pan':
            if stepper.toggle_motor('pan'):
                self.ids.pan_motor.text = "PAN ON"
            else:
                self.ids.pan_motor.text = "PAN OFF"
        else:
            if stepper.toggle_motor('tilt'):
                self.ids.tilt_motor.text = "TILT ON"
            else:
                self.ids.tilt_motor.text = "TILT OFF"

    def pan_start(self):
        stepper.set_pan_start()

    def pan_end(self):
        stepper.set_pan_end()

    def slide_start(self):
        stepper.set_slide_start()

    def slide_end(self):
        stepper.set_slide_end()

    def tilt_start(self):
        stepper.set_tilt_start()

    def tilt_end(self):
        stepper.set_tilt_end()

    def auto_set(self):
        stepper.set_slide_end()
        time.sleep(1)
        stepper.set_pan_end()
        time.sleep(1)
        stepper.set_tilt_end()
        time.sleep(1)
        stepper.set_slide_start()
        time.sleep(1)
        stepper.set_pan_start()
        time.sleep(1)
        stepper.set_tilt_start()
        time.sleep(1)
        print("ALL SET")




    def run_test(self):
        print("SLIDE: " + str(stepper.programed_slide_steps))
        print("PAN: " +  str(stepper.programed_pan_steps))
        print("TILT: " + str(stepper.programed_tilt_steps))
        stepper.slide_programed_test()
        stepper.pan_programed_test()
        stepper.tilt_programed_test()


class MotorPage(Screen):
    def __init__(self, **kwargs):
        super(MotorPage, self).__init__(**kwargs)
        self.temp_value = 1
        self.default_speed = "Speed: " + str(self.temp_value)

    def toggle_motor(self, motor):
        if motor == 'slide':
            if stepper.toggle_motor('slide'):
                self.ids.slide_motor.text = "SLIDE ON"
            else:
                self.ids.slide_motor.text = "SLIDE OFF"
        elif motor == 'pan':
            if stepper.toggle_motor('pan'):
                self.ids.pan_motor.text = "PAN ON"
            else:
                self.ids.pan_motor.text = "PAN OFF"
        else:
            if stepper.toggle_motor('tilt'):
                self.ids.tilt_motor.text = "TILT ON"
            else:
                self.ids.tilt_motor.text = "TILT OFF"

    def set_mode(self, mode):
        global program_mode

        if mode == "video":
            program_mode = "video"
            print("video")
        elif mode == "timelapse":
            program_mode = "timelapse"
            print("timelapse")
        else:
            print("invalid")

    def move_all(self):
        stepper.slide_programed_test()
        stepper.pan_programed_test()
        stepper.tilt_programed_test()

    def find_all_home(self):
        stepper.tilt_home()
        stepper.pan_home()
        stepper.slide_home()

    def find_home_fast(self):
        stepper.fast_home()


class SlidePage(Screen):

    def __init__(self, **kwargs):
        super(SlidePage, self).__init__(**kwargs)
        self.programed_steps = "Programed Steps: " + str(stepper.programed_slide_steps)


    def change_direction(self, direction):
        stepper.change_slide_direction(direction)
        # change direction


    def change_speed(self, speed):
        stepper.slide_speed_setting(speed)


    def set_start(self):
        stepper.set_slide_start()
        self.ids.programed_steps_label.text = "Steps: " + str(stepper.programed_slide_steps)

    def set_end(self):
        stepper.set_slide_end()

    def test_movement(self):
        stepper.slide_programed_test()

    def jog_motor(self):
        stepper.jog_slide()

    def find_home(self):
        stepper.slide_home()

class PanPage(Screen):

    def __init__(self, **kwargs):
        super(PanPage, self).__init__(**kwargs)
        self.programed_steps = "Programed Steps: " + str(stepper.programed_pan_steps)


    def change_direction(self, direction):
        stepper.change_pan_direction(direction)
        # change direction


    def change_speed(self, speed):
        stepper.pan_speed_setting(speed)


    def set_start(self):
        stepper.set_pan_start()
        self.ids.programed_steps_label.text = "Steps: " + str(stepper.programed_pan_steps)

    def set_end(self):
        stepper.set_pan_end()

    def test_movement(self):
        stepper.pan_programed_test()

    def jog_motor(self):
        stepper.jog_pan()

    def find_home(self):
        stepper.pan_home()

class TiltPage(Screen):

    def __init__(self, **kwargs):
        super(TiltPage, self).__init__(**kwargs)
        self.programed_steps = "Steps: " + str(stepper.programed_tilt_steps)


    def change_direction(self, direction):
        stepper.change_tilt_direction(direction)
        # change direction


    def change_speed(self, speed):
        stepper.tilt_speed_setting(speed)


    def set_start(self):
        stepper.set_tilt_start()
        self.ids.programed_steps_label.text = "Programed Steps: " + str(stepper.programed_tilt_steps)

    def set_end(self):
        stepper.set_tilt_end()

    def test_movement(self):
        stepper.tilt_programed_test()

    def jog_motor(self):
        stepper.jog_tilt()

    def find_home(self):
        stepper.tilt_home()



class TimelapseApp(App):
    def build(self):
        return Manager()


if __name__ == '__main__':
    TimelapseApp().run()