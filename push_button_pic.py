import sys,os,time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(24,GPIO.IN)

while True:
	while (GPIO.input(24)==GPIO.HIGH):
		time.sleep(0.5)
	print("Button pressed Take picture")
	os.system("./capture2.sh " + "picbybutton.jpg")
	
	while(GPIO.imput(24)==0):
		time.sleep(0.5)
		
	print("Button released")
