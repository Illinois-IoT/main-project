# Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import speech_recognition as sr

camera = PiCamera()
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

recognizer = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    recognizer.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# App Globals (do not edit)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def get_feed(camera):
    # get camera frames
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        _, image = cv2.imencode(".jpg", image)
        raw_capture.truncate()
        raw_capture.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(get_feed(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/listen')
def transcribe_audio():
    with mic as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
