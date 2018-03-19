from flask import Flask
import requests
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# TODO

# Regularly sync settings from masters /sync endpoint

# Wait for IO input

# 	Take picture with synced settings

#	Upload picture

# 	Re-sync settings

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
 	while True:
 		r = requests.get('http://192.168.1.123/sync')
 		time.sleep(30)
