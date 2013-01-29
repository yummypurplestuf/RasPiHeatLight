from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN)

while True:
	if GPIO.input(11)  == True:
		print "Input! Johnny 5 needs more input!"
