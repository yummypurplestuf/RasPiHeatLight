from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)


while 1:
     GPIO.output(11, False)
     sleep(0)
     GPIO.output(11, True)
     sleep(1)

     GPIO.output(11, False)
     sleep(1)
     GPIO.output(11, True)
     sleep(1)
     GPIO.output(11, False)
     sleep(1)
     GPIO.output(11, True)
     sleep(1)
