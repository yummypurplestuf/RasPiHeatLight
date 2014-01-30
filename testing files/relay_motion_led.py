from time import sleep
import RPi.GPIO as GPIO

fan = 25 				# Pin 1 on 4-Channel Relay
pin2 = 24				# Pin 2 on 4-Channel Relay
pin3 = 8				# Pin 3 on 4-Channel Relay
pin4 = 23				# Pin 4 on 4-Channel Relay
motion_sensor = 11			# Pin for motion sensor input
temp = 4


flash = .1				# Amount of delay

GPIO.setwarnings(False)			
GPIO.setmode(GPIO.BCM)			# GPIO Board init

GPIO.setup(fan, GPIO.OUT)		# Inits the relay connected to the fan
GPIO.setup(pin2, GPIO.OUT)		# "			"
GPIO.setup(pin3, GPIO.OUT)		# "			"
GPIO.setup(pin4, GPIO.OUT)		# "			"
GPIO.setup(motion_sensor, GPIO.IN)	# Inits the Motion Sensor pin
GPIO.setup(temp, GPIO.IN)		# Inits the Temperature Sensor pin

while True:

        if GPIO.input(motion_sensor) == True:

		
                GPIO.output(fan, False)
                print "Intruder"
                sleep(2)
		

        elif GPIO.input(11) == False:

                
		GPIO.output(fan, True)
                #print "Nothing is MOVING"
		
		
		print GPIO.input(temp)
		
        
