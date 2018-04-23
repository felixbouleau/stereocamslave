import requests
import time
import RPi.GPIO as GPIO
import time
import os

SLAVE_ID = None

# TODO

# Regularly sync settings from masters /sync endpoint

# Wait for IO input

# 	Take picture with synced settings


def triggered_callback(channel):
    print('Trigger detected on channel %s. Uploading sample image...'%channel)
    # TODO send static mock picture so we can work on the gif creation and
    # serving from master node
    r = requests.get('http://192.168.1.123/snap/%s' % SLAVE_ID)

    url = "http://192.168.1.123/"
    file_path = "/usr/src/app/sample-img/sample-%s.jpg" % SLAVE_ID
    files = {'file': open(file_path, "rb")}
    requests.post(url, files=files)
    print('Upload completed')

#	Upload picture

# 	Re-sync settings

if __name__ == '__main__':
 	
	# Get slave ID ("which camera in the sequence am I?")
	SLAVE_ID = os.environ["SLAVE_ID"]
	if SLAVE_ID is None:
		raise ValueError('SLAVE_ID env variable not set')
 	GPIO.setmode(GPIO.BCM)
 	channel = 26
 	GPIO.setup(channel, GPIO.IN) #, pull_up_down=GPIO.PUD_DOWN
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

