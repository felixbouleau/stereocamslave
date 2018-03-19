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
    r = requests.get('http://192.168.1.123/sync')

#	Upload picture

# 	Re-sync settings

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
 	channel = [20]
 	GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 	while True:
 		GPIO.add_event_detect(channel, GPIO.RISING, callback=triggered_callback, bouncetime=200)
