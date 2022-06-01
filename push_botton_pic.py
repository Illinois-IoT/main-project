import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import datetime
import time
import os

def button_callback(channel):
    print("Button was pushed!")
    current_time = datetime.datetime.now()
    time_formatted = current_time.strftime("%m_%d_%Y--%H_%M_%S")
    os.system("./capture2.sh " + time_formatted + ".jpg")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback,bouncetime=200) # Setup event on pin 10 rising edge, ignoring further edges for 200ms
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
