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
desired_temp = 75                   # The temperature you would like it to be           

###################################################################################

GPIO.setwarnings(False)         
GPIO.setmode(GPIO.BCM)              # GPIO Board init

GPIO.setup(fan, GPIO.OUT)           # Inits the relay connected to the fan
GPIO.setup(light_bank_1, GPIO.OUT)  # "         "
GPIO.setup(light_bank_2, GPIO.OUT)  # "         "
GPIO.setup(light_bank_3, GPIO.OUT)  # "         "
GPIO.setup(motion_sensor, GPIO.IN)  # Inits the Motion Sensor pin
GPIO.setup(temp, GPIO.IN)           # Inits the Temperature Sensor pin



def main():
    motion = get_motion()
    temp_sensor = get_temp_and_humidity()
    fahrenheit = temp_sensor[0]
    humidity = temp_sensor[1]
    get_date_and_time = get_date_and_time()
    date = get_date_and_time[0]
    time = get_date_and_time[1]



def get_temp_and_humidity():
    temperature_list = []
    humidity_list = []
    
    while temperature_list or humidity_list < 50:            
        # Run the DHT program to get the humidity and temperature readings!
        output = subprocess.check_output(["./Adafruit_DHT", "11", "4"])
        
        # search output and match temperature and humidity values
        temperature_match = re.search("Temp =\s+([0-9.]+)", output)
        humidity_match = re.search("Hum =\s+([0-9.]+)", output)

        # compare temperature_match and humidity_match against None to make sure good data was recieved
        if (not temperature_match) and (not humidity_match):
            # Add temperature and humidity to their respective lists
            humidity_list.append(float(humidity_match.group(1)))
            temperature_list.append(float(temperature_match.group(1)))            
        
        # waits 3 seconds if bad data was recieved from temp sensor
        else:
            sleep(3)

    humidity = sum(humidity_list)/ len(humidity_list) 
    temperature = sum(temperature_list)/ len(temperature_list)     
    
    # Convert temp from C to F
    fahrenheit = temperature*1.8+32
    
    """
        Printing of the data recieved from the temperature and humidity sensor
    """
    print
    print "---------------------------------------"
    print "Current Conditions Are:"
    print
    print "Temperature: %.1f F" % fahrenheit
    print "Humidity:    %.1f %%" % humidity
    print "----------------------------------------"
    print

    return fahrenheit, humidity


def fan(fahrenheit):
    # TODO: get outside temperature from website (http://www.weather.com/) using mechanize 

    if desired_temp < fahrenheit:
        GPIO.output(fan, True)
    else:
        GPIO.output(fan, False)

    """
    eventually the code needs to look like:

    get outside_temperature and compare it against the month 
    and depending on the month and outside temperature it can 
    be assumed which season it is and whether or not turning the 
    fan on will blow either hot or cold air

    because the fan is just blowing air over a radiator supplied 
    by either cold or hot water (depending on the season) you must 
    know which one it is in order to heat or cool the room accordingly


    """



def lights(motion):
    # sets the lights on or off depending on motion being detected in the room
    # TODO: add a timing system to delay turning lights off after a period of time
    GPIO.output(light_bank_1, motion)
    sleep(3)
    GPIO.output(light_bank_2, motion)
    sleep(3)
    GPIO.output(light_bank_2, motion)
    sleep(3)


def get_motion():
    if GPIO.input(motion_sensor)  == True:
        motion = False
    else:
        motion = True
    
    print 'motion is: ', motion 
    return motion


def get_outdoor_temperature():
    # will be used later on
    pass


def get_date_and_time():
    # need to get current date and time and return those values
    current_date_and_time = datetime.datetime.now()
    month = str(current_date_and_time.month)
    day = str(current_date_and_time.day)
    year = str(current_date_and_time.year)
    hour = str(current_date_and_time.hour)
    minute = str(current_date_and_time.minute)

    date = month+'/' + day+'/' + year
    time = hour+':' + minute
    return date, time


def post_to_google_spreadsheet(fahrenheit, humidity, motion, date, time):


    """ 
    
    These are used for login information with Google Spread sheet, create a "password.txt" file and type your password in there for authentication 
    to Google. Be sure to remember to add "password.txt" to your ".gitignore" file if you are using Git/GitHub so that you don't post your password
    to the entire world.
    
    email       = 'email@gmail.com'
    password    = linestring = open('password.txt', 'r').read()
    spreadsheet = 'Computer Science Lab Temperature'
    """


    user_info = open('/home/pi/rasp_heat/user_info.txt', 'r')
    user_name = user_info.readline()
    user_pass = user_info.readline()
    spreadsheet = 'Computer Science Lab Temperature'
    user_info.close()

                # Login with your Google account
    try:
        gc = gspread.login(user_name, user_pass)
        print "Attempting to Login"
    except:
        print "Unable to log in.  Check your email address/password"
        

    # Open a worksheet from your spreadsheet using the filename
    try:
        worksheet = gc.open(spreadsheet).sheet1
        # Alternatively, open a spreadsheet using the spreadsheet's key
        # worksheet = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
    except:
        print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
        sys.exit()

if __name__ == "__main__": main()