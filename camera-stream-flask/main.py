#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import subprocess

camera = PiCamera()
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_camera_frame(camera):
    #get camera frames
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        _, image = cv2.imencode(".jpg", image)
        raw_capture.truncate()
        raw_capture.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n\r\n')

def get_live_transcription():
    popen = subprocess.Popen("spchcat", stdout=subprocess.PIPE)
    for stdout_line in iter(popen.stdout.readline, b""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

@app.route('/video_feed')
def video_feed():
    return Response(get_camera_frame(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/transcript_feed')
def transcript_feed():
    return Response(get_live_transcription(camera),
                    mimetype='mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
