import requests
import time
import RPi.GPIO as GPIO
import time

# TODO

# Regularly sync settings from masters /sync endpoint

# Wait for IO input

# 	Take picture with synced settings


def triggered_callback(channel):
    print('This is a edge event callback function!')
    print('Edge detected on channel %s'%channel)
    print('This is run in a different thread to your main program')
    # TODO send static mock picture so we can work on the gif creation and
    # serving from master node
    r = requests.get('http://192.168.1.123/sync')

#	Upload picture

# 	Re-sync settings

if __name__ == '__main__':
 	GPIO.setmode(GPIO.BCM)
 	channel = 26
 	GPIO.setup(channel, GPIO.IN) #, pull_up_down=GPIO.PUD_DOWN
	print('Starting edge event monitoring')
	GPIO.add_event_detect(channel, GPIO.RISING, callback=triggered_callback, bouncetime=200)
	while True:
		time.sleep(10)
		print('Still waiting...')
	print('Stopping (?)')

