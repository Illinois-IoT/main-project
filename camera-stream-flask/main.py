#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

pi_camera = PiCamera()
pi_camera.resolution = (640, 480)
raw_capture = PiRGBArray(pi_camera, size=(640, 480))

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    #get camera frame
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        _, image = cv2.imencode(".jpg", image)
        raw_capture.truncate()
        raw_capture.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods = ['POST'])
def upload_audio():
    if request.method == 'POST':
        f = request.files['audio_data']
        f.save(secure_filename(f.filename))
        return "File saved successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
