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


import time
import RPi.GPIO as GPIO
import subprocess
import re
import datetime
import sys
import gspread
import mechanize



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
    post_to_google_spreadsheet(date, time, fahrenheit, humidity, motion)



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
            time.sleep(3)

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
    time.sleep(3)
    GPIO.output(light_bank_2, motion)
    time.sleep(3)
    GPIO.output(light_bank_2, motion)
    time.sleep(3)


def get_motion():
    if GPIO.input(motion_sensor)  == True:
        motion = False
    else:
        motion = True
    
    print 'motion is: ', motion 
    return motion


def get_outdoor_temperature():
    # will be used later on using mechanize 
    # Generates a web browser instance 
    # Opens www.whatsmyip.com/ and gets external IP address
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent makes the destination website think it's from a real person
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    html = br.open('http://www.weather.com/')
    html = html.read()
    html = unicode(html, errors='ignore')
    
    # for f in br.forms():
    #     print f
    # select the form on the website
    br.select_form(nr=0)
    # input location in search box
    br['where'] = "Olivet, MI"
    html = br.submit()
    html = html.read()
    outside_list = []
    # matches temperature and unit, then append it to a list
    match = re.search('<span itemprop="temperature-fahrenheit">(\d*)</span>', html)
    outside_list.append(match.group(1))
    match = re.search('<span class="wx-unit">(.)</span>', html) 
    
    outside_list.append(u'\xb0'.encode("UTF-8") + match.group(1))
    return outside_list


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


def post_to_google_spreadsheet(date, time, fahrenheit, humidity, motion):

    """ 
    These are used for login information with Google Spread sheet, create a user_info.txt file in the same directory as the automate.py file.
    In the user_info.txt file add:
    
    email@gmail.com
    password
    
    save the file and add user_info.txt to your .gitignore file within the directory.
    I will soon be adding crontab support as well.
    Don't forget to create a Google Spreadsheet and change the 'Computer Science Lab Temperature' down below to the name of your spreadsheet file.
    """


    user_info = open('/home/pi/RasPiHeatLight/user_info.txt', 'r')
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