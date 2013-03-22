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



import gspread
from time import sleep
import RPi.GPIO as GPIO
import os
import subprocess
import re
import datetime
import time
import sys

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
    tempList = []
    humList = []
    runTime = 50
    while len(tempList) < runTime:
        # Run the DHT program to get the humidity and temperature readings!
        output = subprocess.check_output(["./Adafruit_DHT", "11", "4"])
        # search for temperature printout
        valid_temp = re.search("Data \(([\d]+)\):", output)
        valid_temp = int(valid_temp.group(1))
        if valid_temp == 40:
            matches = re.search("Temp = ([\d]+) \*C, Hum = ([\d]+) %", output)
            if not matches == None:

                temperature = float(matches.group(1))
                humidity = float(matches.group(2))
                
                # Convert temp from C to F
                temperature = temperature * 1.8 + 32
                #print 
                #print
                #print "Temperature: %.1f F" % temperature
                #print "Humidity:    %.1f %%" % humidity
                tempList.append(temperature)
                humList.append(humidity)

                if len(tempList) == runTime:
                    temperature = sum(tempList) / len(tempList)
                    humidity = sum(humList) / len(humList)
                    print temperature, humidity
                    gSpread(temperature, humidity)

def gSpread(temperature, humidity):


    email       = 'jared.luellen@cs.olivetcollege.edu'
    password    = linestring = open('password.txt', 'r').read()
    spreadsheet = 'Computer Science Lab Temperature'

    # Login with your Google account
    try:
        gc = gspread.login(email, password)
    except:
        print "Unable to log in.  Check your email address/password"
        sys.exit()

    # Open a worksheet from your spreadsheet using the filename
    try:
        worksheet = gc.open(spreadsheet).sheet1
        # Alternatively, open a spreadsheet using the spreadsheet's key
        # worksheet = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
    except:
        print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
        sys.exit()

    val = worksheet.cell(2, 10).value
    val = int(val)
    print val

    while val > 1:
        now = datetime.datetime.now()
        date =  datetime.date.today().strftime("%m %d %Y")
        current_time = time.strftime( "%H:%M:%S")
        motion = True 
        print temperature, humidity
        try:
            val += 1
            values = [date,current_time, temp, humidity, motion]
        

            worksheet.update_cell(val, 1, date)
            worksheet.update_cell(val, 2, current_time)
            worksheet.update_cell(val, 3, temperature)
            worksheet.update_cell(val, 4, humidity)
            worksheet.update_cell(val, 5, motion)

            worksheet.update_cell(2, 10, val)

            print "Wrote a row to %s" % spreadsheet
            time.sleep(0)
            print val
            break

        
        except:
            print "Unable to append data.  Check your connection?"
            sys.exit()



def getMotion():
    pass




while True:
    getTemp()
    
