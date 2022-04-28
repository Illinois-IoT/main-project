import RPi.GPIO as GPIO
import pyaudio
import audioop

LED = 27
CHUNK = 1024
FORMAT = pyaudio.paInt16
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
VOLUME_THRESHOLD = 2000

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

try:
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    while True:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, WIDTH)
        if rms > VOLUME_THRESHOLD:
            print( "Sound Detected!")
            GPIO.output(LED, GPIO.HIGH)
        else:
            GPIO.output(LED, GPIO.LOW)
except:
    stream.stop_stream()
    stream.close()
    p.terminate()
finally:
    GPIO.cleanup()