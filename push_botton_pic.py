import sys
import os
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if(GPIO.input(10) == GPIO.LOW):
        print("Hello")
        time.sleep(0.5)
