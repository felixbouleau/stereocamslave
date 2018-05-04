import requests
import time
import RPi.GPIO as GPIO
import time
import os
import picamera
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json
import imageio
from PIL import Image

# master
UPLOAD_FOLDER = '/usr/src/app/img/'
OUTPUT_FOLDER = '/usr/src/app/output/'
TMP_FOLDER = '/usr/src/app/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'jpeg'])
DUMMY_SYNC_RESPONSE = {"exposure": "auto", "wb": 1234, "filename": "test.jpg"}

# Web server (master)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# slave
SLAVE_ID = None
CAMERA = None
IS_MASTER = None


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)

def create_gif(sequence_id):
    print("Creating gif from sequence '%s'" % sequence_id)
    wanted_filename = "/usr/src/app/output/%s.gif" % sequence_id
    all_filenames = sorted(os.listdir(UPLOAD_FOLDER))
    wanted_inputs = []
    gif_frames = []
    for file in all_filenames:
        # Only consider images that are part of the current sequence
        # (i.e. `<correct sequence id>-<some serial number>.gif`)
        if file.split("-")[0] == sequence_id:
            resize_image(UPLOAD_FOLDER + file,
                         TMP_FOLDER + file,
                         size=(800, 800))
            gif_frames.append(imageio.imread(TMP_FOLDER + file))
            os.remove(TMP_FOLDER + file)

    gif_frames_boomerang = list(gif_frames) + list(reversed(gif_frames))
    
    # Save as gif
    imageio.mimsave(wanted_filename, gif_frames_boomerang)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'],
                               filename)

@app.route('/sync')
def hello_world():
    return jsonify(DUMMY_SYNC_RESPONSE)

@app.route('/makegif/<sequence_id>')
def makegifendpoint(sequence_id):
    create_gif(sequence_id)
    #return redirect(url_for('output_file',
    #                filename="sample.gif"))
    return send_from_directory(app.config['OUTPUT_FOLDER'],
                               "%s.gif" % sequence_id)

def triggered_callback(channel):
    print('Trigger detected on channel %s. Uploading sample image...' % channel)
    camera.capture('/data/%s.jpg') % SLAVE_ID
    url = "http://192.168.1.123/"
    file_path = "/data/%s.jpg" % SLAVE_ID
    files = {'file': open(file_path, "rb")}
    requests.post(url, files=files)
    print('Upload completed')

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

def start_as_master():
    # Start flask server for syncing settings and receiving
    # images from slaves
    app.run(host='0.0.0.0', port=80)# , debug=True)

    #while True:
    #    print('pretending to do server things...')
    #    time.sleep(60)

if __name__ == '__main__':
    # Get slave ID ("which camera in the sequence am I?")
    
    SLAVE_ID = os.environ.get("SLAVE_ID")
    IS_MASTER = os.environ.get("IS_MASTER")
    
    # Set up camera if it isn't already
    if CAMERA != None:
        CAMERA = picamera.PiCamera()
        CAMERA.resolution = (1024, 768)
        CAMERA.start_preview()

    if IS_MASTER is not None:
        print('Is master!')
        start_as_master()
    else:
        print('Is slave!')
        start_as_slave()
