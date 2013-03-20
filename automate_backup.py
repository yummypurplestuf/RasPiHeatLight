# !/usr/bin/python 
#
# Author: Jared R. Luellen, Created: Feb. 2013
#
# This program aims to aid in making the home enviroment easier and more manageable.
# As our lives become more mobile it's more accesible now more than ever to control
# appliances from your mobile phone or laptop computer.

########################################################################
# INFO: 

#           Lighting Scheme
# 32w per overhead bulb, bank 1 = 192w, 192w/120v = 1.6A
# 32w per overhead bulb, bank 2 = 192w, 192w/120v = 1.6A
# 32w per overhead bulb, bank 3 = 256w, 256w/120v = 2.13A

#           Electric Motor 
# 1 hp = 745.699872w, 1/6hp motor = 124.9499w, 124.9499w/120v = 1.0413A
#########################################################################







from time import sleep
import RPi.GPIO as GPIO
import os
import subprocess
import re
import datetime
import time


fan = 25                            # Pin 1 on 4-Channel Relay
light_bank_1 = 24                   # Pin 2 on 4-Channel Relay
light_bank_2 = 8                    # Pin 3 on 4-Channel Relay
light_bank_3 = 23                   # Pin 4 on 4-Channel Relay
motion_sensor = 11                  # Pin for Motion Sensor Input
temp = 4                            # Pin for Temperature/Humidity Sensor
now = datetime.datetime.now()       # Grabs current time and date
later = datetime.datetime.now()     # Grabs current time and date
motion = False              
gettemp = True
desired_temp = 75                   # The temperature you would like it to be
temp_sensor = 0             

###################################################################################
###################################################################################

GPIO.setwarnings(False)         
GPIO.setmode(GPIO.BCM)              # GPIO Board init

GPIO.setup(fan, GPIO.OUT)           # Inits the relay connected to the fan
GPIO.setup(light_bank_1, GPIO.OUT)  # "         "
GPIO.setup(light_bank_2, GPIO.OUT)  # "         "
GPIO.setup(light_bank_3, GPIO.OUT)  # "             "
GPIO.setup(motion_sensor, GPIO.IN)  # Inits the Motion Sensor pin
GPIO.setup(temp, GPIO.IN)           # Inits the Temperature Sensor pin


def getTemp():
    # Run the DHT program to get the humidity and temperature readings!
    temperature_matches = None
    humidity_matches = None

    while not matches:
        output = subprocess.check_output(["./Adafruit_DHT", "11", "4"])
        print output
    # search for temperature printout
        temperature_matches = re.search("Temp =\s+([0-9.]+)", output)
        humidity_matches = re.search("Hum =\s+([0-9.]+)", output)

        temp_sensor = float(matches.group(1))
        humidity = float(matches.group(1))

        # Convert temp from C to F
        temp_sensor = temp_sensor * 1.8 + 32
        print "Current Conditions Are:"
        print
        print "Temperature: %.1f F" % temp_sensor
        print "Humidity:    %.1f %%" % humidity

while True:
    getTemp()
