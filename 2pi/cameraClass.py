from subprocess import call
import time
from datetime import datetime
from datetime import timedelta
import subprocess


from wrappers import GPhoto


camera_wrapper = GPhoto(subprocess)

CONFIGS = [("1/8000", 100),
           ("1/6400", 100),
           ("1/5000", 100),
           ("1/4000", 100),
           ("1/3100", 100),
           ("1/2500", 100),
           ("1/1000", 100),
           ("1/1600", 100),
           ("1/1250", 100),
           ("1/1000", 100),
           ("1/800", 100),
           ("1/640", 100),
           ("1/500", 100),
           ("1/400", 100),
           ("1/320", 100),
           ("1/250", 100),
           ("1/100", 100),
           ("1/160", 100),
           ("1/125", 100),
           ("1/100", 100),
           ("1/80", 100),
           ("1/60", 100),
           ("1/50", 100),
           ("1/40", 100),
           ("1/30", 100),
           ("1/25", 100),
           ("1/20", 100),
           ("1/15", 100),
           ("1/13", 100),
           ("1/10", 100),
           ("1/8", 100),
           ("1/6", 100),
           ("1/5", 100),
           ("1/4", 100),
           ("0.3", 100),
           ("0.4", 100),
           ("0.5", 100),
           ("0.6", 100),
           ("0.8", 100),
           ("1", 100),
           ("1.3", 100),
           ("1.6", 100),
           ("2", 100),
           ("2.5", 100),
           ("3.2", 100),
           ("4", 100),
           ("5", 100),
           ("6", 100),
           ("8", 100),
           ("10", 100),
           ("13", 100),
           ("15", 100),
           ("20", 100),
           ("25", 100),
           ("30", 100),
           ("30", 100)]


class CameraObj(object):
    def __init__(self):
        self.picture_count = 0
        self.total_pictures = 0
        self.timelapse_duration = 60
        self.timelapse_interval = 3
        self.timelape_start_time = time.time()
        self.shutter_time = 0.5
        self.stable_delay = 0.5

        self.set_timelapse(self.timelapse_duration, self.timelapse_interval)

    def set_timelapse(self, duration, interval):
        # duration in min
        # interval in seconds
        self.total_pictures = int((duration * 60) / interval)
        self.timelapse_duration = duration
        self.timelapse_interval = interval
        self.clip_duration = int(self.total_pictures / 24)


    def get_config(self):
        camera_wrapper.get_shutter_speeds()
        camera_wrapper.get_isos()

    def reset_timelapse(self):
        self.total_pictures = int((self.timelapse_duration * 60) / self.timelapse_interval)
        self.clip_duration = int(self.total_pictures / 24)


    def set_interval(self, direction):
        if direction < 0:
            self.timelapse_interval -= 1
        else:
            self.timelapse_interval += 1

        if self.timelapse_interval < 1:
            self.timelapse_interval = 1
        
        self.reset_timelapse()

    def set_duration(self, direction):
        if direction < 0:
            self.timelapse_duration -= 5
        else:
            self.timelapse_duration += 5
        if self.timelapse_duration < 5:
            self.timelapse_duration = 5
        self.reset_timelapse()

    def modify_bulb_time(self, direction):
        if direction < 0:
            self.shutter_time -= 0.025
        else:
            self.shutter_time += 0.025

    def initialize_camera(self):
        camera_wrapper.set_capture_target()

    def initialize(self):
        camera_wrapper.set_capture_target()

    def trigger(self):
        camera_wrapper.trigger()

    def timelapse_picture(self):
        time.sleep(self.stable_delay)
        self.capture_image()
        print("PIC")
        self.picture_count += 1


    def capture_image(self):
        camera_wrapper.capture_image()

    def bulb_trigger(self):
        camera_wrapper.bulb_trigger(self.shutter_time)


camera = CameraObj()



   

  