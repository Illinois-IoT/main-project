# Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import select
import os
import speech_recognition as sr

camera = PiCamera()
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

r = sr.Recognizer()
m = sr.Microphone(device_index=2)
with m as source:
    # we only need to calibrate once, before we start listening
    r.adjust_for_ambient_noise(source)
read_end, write_end = os.pipe()

# App Globals (do not edit)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def get_camera_frame(camera):
    # get camera frames
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        _, image = cv2.imencode(".jpg", image)
        raw_capture.truncate()
        raw_capture.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n\r\n')


def get_live_transcription():
    while select.select([read_end], [], [], 0)[0]:
        chunk = os.read(read_end)
        yield chunk + "<br>"


@app.route('/video_feed')
def video_feed():
    return Response(get_camera_frame(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# TODO try using Service Sent Events for better performance
@app.route('/transcript_feed')
def transcript_feed():
    # TODO: https://stackoverflow.com/questions/18614301/keep-overflow-div-scrolled-to-bottom-unless-user-scrolls-up/60546366#60546366
    return Response(get_live_transcription(),
                    mimetype='text/html')


def listener_callback(recognizer, audio):
    try:
        os.write(write_end, recognizer.recognize_google(audio).encode())
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, listener_callback)
# `stop_listening` is now a function that, when called, stops background listening


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
