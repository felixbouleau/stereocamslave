import requests
import time
import RPi.GPIO as GPIO
import time
import os
import picamera

SLAVE_ID = None
CAMERA = None
IS_MASTER = None

# TODO

# Regularly sync settings from masters /sync endpoint

# Wait for IO input

#   Take picture with synced settings

def triggered_callback(channel):
    print('Trigger detected on channel %s. Uploading sample image...' % channel)
    camera.capture('/data/%s.jpg') % SLAVE_ID
    url = "http://192.168.1.123/"
    file_path = "/data/%s.jpg" % SLAVE_ID
    files = {'file': open(file_path, "rb")}
    requests.post(url, files=files)
    print('Upload completed')

#   Upload picture

#   Re-sync settings

def start_as_slave():
    GPIO.setmode(GPIO.BCM)
    channel = 26
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print('Starting edge event monitoring')
    GPIO.add_event_detect(channel,
                          GPIO.RISING,
                          callback=triggered_callback,
                          bouncetime=5000)
    while True:
        # TODO actually sync settings..
        print('Syncing settings')
        r = requests.get('http://192.168.1.123/sync')
        time.sleep(5)
    print('Stopping (?)')

if __name__ == '__main__':
    # Set up camera
    CAMERA = picamera.PiCamera()
    CAMERA.resolution = (1024, 768)
    CAMERA.start_preview()

    # Get slave ID ("which camera in the sequence am I?")
    SLAVE_ID = os.environ["SLAVE_ID"]
    IS_MASTER = os.environ["IS_MASTER"]
    if IS_MASTER is not None:
        print('Is master!')
        start_as_master()
    else:
        print('Is slave!')
        start_as_slave()

