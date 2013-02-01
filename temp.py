from time import sleep
import RPi.GPIO as GPIO
import subprocess
import re

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

  
while(True):
	# Run the DHT program to get the humidity and temperature readings!

	output = subprocess.check_output(["./Adafruit_DHT", "11", "4"]);
	print output
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

	print "Temperature: %.1f f" % temp
	print "Humidity:    %.1f %%" % humidity
	print
	print "---------------------------------"

