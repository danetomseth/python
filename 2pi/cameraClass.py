from subprocess import call
import time


class CameraObj(object):
    def __init__(self):
        self.picture_count = 0
        self.total_pictures = 0
        self.timelapse_duration = 60
        self.timelapse_interval = 3
        self.timelape_start_time = time.time()
        self.shutter_time = 0.5

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

    def modify_bulb_time(self, direction):
        if direction < 0:
            self.shutter_time -= 0.025
        else:
            self.shutter_time += 0.025



    def bulb_picture(self):
        msTime = self.shutter_time * 1000
        delaySetting = "--wait-event=" + str(msTime) + "ms"
        call (["gphoto2","--set-config", "eosremoterelease=2", delaySetting, "--set-config", "eosremoterelease=4"])


    def manual_bulb(self):
        call (["gphoto2","--set-config", "eosremoterelease=5"])
        time.sleep(self.shutter_time)
        call (["gphoto2","--set-config", "eosremoterelease=4"])


    def initiate_timelapse(self):
        self.timelapse_start_time = time.time()
        self.picture_count = 0

    def timelapse_picture(self):
        self.focus_picture()
        self.picture_count += 1

    def capture_image(self):
        print("PICTURE!")
        # call (["gphoto2","--capture-image"])

    def quick_picture(self):
        call (["gphoto2","--set-config", "eosremoterelease=2"])
        print("PIC")

    def focus_picture(self):
        call (["gphoto2","--set-config", "eosremoterelease=6","--set-config", "eosremoterelease=2"])
        call (["gphoto2","--set-config", "eosremoterelease=4"])
        print("PIC")

    def test_capture(self):
        print("PICTURE!")
        call (["gphoto2","--capture-image"])


    def set_target(self):
        call (["gphoto2","--set-config", "capturetarget=1"])