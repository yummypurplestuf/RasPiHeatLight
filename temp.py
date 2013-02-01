from time import sleep
import RPi.GPIO as GPIO
import subprocess
import re
import datetime
import time
fan = 25 				# Pin 1 on 4-Channel Relay
light_bank_1 = 24			# Pin 2 on 4-Channel Relay
light_bank_2 = 8			# Pin 3 on 4-Channel Relay
light_bank_3 = 23			# Pin 4 on 4-Channel Relay
motion_sensor = 11			# Pin for motion sensor input
temp = 4
now = datetime.datetime.now()
later = datetime.datetime.now()
motion = False
gettemp = True
desired_temp = 72
temp_sensor = 0




flash = .1				# Amount of delay

GPIO.setwarnings(False)			
GPIO.setmode(GPIO.BCM)			# GPIO Board init

GPIO.setup(fan, GPIO.OUT)		# Inits the relay connected to the fan
GPIO.setup(light_bank_1, GPIO.OUT)		# "			"
GPIO.setup(light_bank_2, GPIO.OUT)		# "			"
GPIO.setup(light_bank_3, GPIO.OUT)		# "			"
GPIO.setup(motion_sensor, GPIO.IN)	# Inits the Motion Sensor pin
GPIO.setup(temp, GPIO.IN)		# Inits the Temperature Sensor pin


  
while(True):
	
			
	def __init__(self, now, later):
				
				
		now = datetime.datetime.now()
		later = datetime.datetime.now()
		now2= datetime.time(now.hour, now.minute, now.second)
		later2 = datetime.time(now.hour, now.minute, now.second)
		


        def getTemp():
		
		gettemp = True

                # Run the DHT program to get the humidity and temperature readings!
                while gettemp == True:
		             		  	
                	output = subprocess.check_output(["./Adafruit_DHT", "11", "4"]);

                        # search for temperature printout
                	matches = re.search("Temp =\s+([0-9.]+)", output)
                	if (not matches):
				sleep(3)
                        	continue
                	temp = float(matches.group(1))

                        # search for humidity printout
                	matches = re.search("Hum =\s+([0-9.]+)", output)
                	if (not matches):
                		sleep(3)
                        	continue
                	humidity = float(matches.group(1))

                        # Convert temp from C to F
                	temp = temp*1.8+32
			temp_sensor = temp
		        if temp == 77:
				gettemp = False
			global temp_sensor
                	
			print
			print "---------------------------------------"
			print "Current Conditions Are:"
			print
                	print "Temperature: %.1f F" % temp_sensor
                	print "Humidity:    %.1f %%" % humidity
                	print "----------------------------------------"
			gettemp = False
			
	def motionTrue(now, motion):
		if GPIO.input(motion_sensor) == True:
			
			motion = True

			now = datetime.datetime.now()
			
			if temp_sensor > desired_temp:
				GPIO.output(fan, True)			
			
			if temp_sensor < desired_temp:
				GPIO.output(fan, False)
			
			
			
				
			GPIO.output(light_bank_1, False)
       	       		sleep(1)
     	
       			GPIO.output(light_bank_2, False)
			sleep(1)

       			GPIO.output(light_bank_3, False)
       			sleep(1)
			print "Motion"

	def motionFalse(later, motion):
		if GPIO.input(motion_sensor) == False:
			GPIO.output(fan, True)
               		GPIO.output(light_bank_1, True)
    	       		GPIO.output(light_bank_2, True)
       	       		GPIO.output(light_bank_3, True)
			
			print "Turning devices OFF"
		

	if GPIO.input(motion_sensor) == True:
		
		temp_sensor
		motion = True
		motionTrue(now, motion)
		getTemp()
		
	if GPIO.input(motion_sensor) == False:
		temp_sensor
		motion = False		
		
                if later > now.replace(hour=0, minute=0, second=5, microsecond=0):
			motionFalse(later, motion)

