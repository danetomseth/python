from subprocess import call
import time


class CameraObj(object):
    def __init__(self):
        self.picture_count = 0
        self.total_pictures = 0
        self.timelapse_duration = 60
        self.timelapse_interval = 3

        self.set_timelapse(self.timelapse_duration, self.timelapse_interval)

    def set_timelapse(self, duration, interval):
        # duration in min
        # interval in seconds
        self.total_pictures = int((duration * 60) / interval)
        self.timelapse_duration = duration
        self.timelapse_interval = interval
        self.clip_duration = int(self.total_pictures / 24)
        print("TOTAL FRAMES: " + str(self.total_pictures))

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

    def capture_image():
        print("PICTURE!")
        # call (["gphoto2","--capture-image"])