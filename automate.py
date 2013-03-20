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
import sys
import gspread



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

GPIO.setwarnings(False)         
GPIO.setmode(GPIO.BCM)              # GPIO Board init

GPIO.setup(fan, GPIO.OUT)           # Inits the relay connected to the fan
GPIO.setup(light_bank_1, GPIO.OUT)  # "         "
GPIO.setup(light_bank_2, GPIO.OUT)  # "         "
GPIO.setup(light_bank_3, GPIO.OUT)  # "             "
GPIO.setup(motion_sensor, GPIO.IN)  # Inits the Motion Sensor pin
GPIO.setup(temp, GPIO.IN)           # Inits the Temperature Sensor pin


  
while(True):
    
            
    def gSpread():


        """ These are used for login information with Google Spread sheet, create a "password.txt" file and type your password in there for authentication 
            to Google. Be sure to remember to add "password.txt" to your ".gitignore" file if you are using Git/GitHub so that you don't post your password
            to the entire world.
        """


        email       = 'jared.luellen@cs.olivetcollege.edu'
        password    = linestring = open('password.txt', 'r').read()
        spreadsheet = 'Computer Science Lab Temperature'

                    # Login with your Google account
        try:
            gc = gspread.login(email, password)
            print "try gSpread"
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
            

            """
                Printing of the data recieved from the temperature and humidity sensor
            """
            print
            print "---------------------------------------"
            print "Current Conditions Are:"
            print
            print "Temperature: %.1f F" % temp_sensor
            print "Humidity:    %.1f %%" % humidity
            print "----------------------------------------"
            print

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

    def postData(temp_sensor, humidity, motion):

        val = worksheet.cell(2, 10).value
        val = int(val)

        while val > 0:     
            now = datetime.datetime.now()

            date =  datetime.date.today().strftime("%m %d %Y")
            current_time = time.strftime( "%H:%M:%S") 

            try:
                values = [date, current_time, temp_sensor, humidity, motion]

                worksheet.update_cell(val, 1, date)
                worksheet.update_cell(val, 2, current_time)
                worksheet.update_cell(val, 3, temp_sensor)
                worksheet.update_cell(val, 4, humidity)
                worksheet.update_cell(val, 5, motion)

                worksheet.update_cell(2, 10, val)  # Updates the cell which keeps track of the current row

            except:
                print "Unable to append data.  Check your connection?"
                sys.exit()

                # Wait 30 seconds before continuing
            print "Wrote a row to %s" % spreadsheet
            time.sleep(0)
            val += 1
            print val
