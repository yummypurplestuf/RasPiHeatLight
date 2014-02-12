from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

fan = 25                            # Pin 1 on 4-Channel Relay
light_bank_1 = 24                   # Pin 2 on 4-Channel Relay
light_bank_2 = 8                    # Pin 3 on 4-Channel Relay
light_bank_3 = 23                   # Pin 4 on 4-Channel Relay

GPIO.setup(fan, GPIO.OUT)           # Inits the relay connected to the fan
GPIO.setup(light_bank_1, GPIO.OUT)  # "         "
GPIO.setup(light_bank_2, GPIO.OUT)  # "         "
GPIO.setup(light_bank_3, GPIO.OUT) 


while 1:
     GPIO.output(fan, True)
     GPIO.output(light_bank_1, True)
     GPIO.output(light_bank_2, True)
     GPIO.output(light_bank_3, True)
     print "True"
     sleep(3)
     GPIO.output(fan, False)
     GPIO.output(light_bank_1, False)
     GPIO.output(light_bank_2, False)
     GPIO.output(light_bank_3, False)
     print "False"
     sleep(3)