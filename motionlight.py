from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(11, GPIO.IN)


motion = False
while True:
		
	
	if GPIO.input(11) == True:
		GPIO.output(22, False)
		print "Intruder"
		sleep(2)
		
	if GPIO.input(11) == False:
		GPIO.output(22, True)
		print "Nothing is MOVING"

	
