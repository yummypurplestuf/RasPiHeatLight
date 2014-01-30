import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup (7, GPIO.OUT)

GPIO.setwarnings(False)

while True:
	GPIO.output(7, True)
	time.sleep(3)
	GPIO.output(7, False)
	time.sleep(1)
