import sys
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	# TODO: could try to use callback
    if (GPIO.input(24) == GPIO.LOW):
        print("Button pressed Take picture")
        os.system("./capture2.sh " + "picbybutton.jpg")
        time.sleep(0.5)

        if (GPIO.input(24) == GPIO.HIGH):
            print("Button released")
