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
import os
import gspread
import mechanize



fan_motor = 25                      # Pin 1 on 4-Channel Relay
light_bank_1 = 24                   # Pin 2 on 4-Channel Relay
light_bank_2 = 8                    # Pin 3 on 4-Channel Relay
light_bank_3 = 23                   # Pin 4 on 4-Channel Relay
motion_sensor = 11                  # Pin for Motion Sensor Input
temp = 4                            # Pin for Temperature/Humidity Sensor
desired_temp = 75                   # The temperature you would like it to be           
false_time_list = []
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
    temp = get_temp_and_humidity()
    motion = get_motion()
    outside = get_outdoor_temperature()
    date_time =  get_date_and_time()
    external_ip = get_external_ip()
    
    while True:
        
        motion = get_motion()
        motion_detected_time = motion[1]
        motion = motion[0]
        lights(motion, motion_detected_time)
        temperature = get_temp_and_humidity()
        fahrenheit = temperature[0]
        humidity = temperature[1]
        current_air_value = fan(fahrenheit)
        print current_air_value

        
        time.sleep(1)



    
def get_temp_and_humidity():
    """
    Runs a C file that interacts with the DHT11 sensor, matches the temperature and humidity
        off of the standard output from the program and then adds those values to seperate list
        so that the temperature and humidity values can be averaged out in order to get more 
        accurate values.
    """
    temperature_list = []
    humidity_list = []
    while len(temperature_list) < 3:
        # Run the DHT program to get the humidity and temperature readings!
        output = subprocess.check_output(["./Adafruit_DHT", "11", "4"])
        match = re.search('Temp = ([0-9]+) \*C, Hum = ([0-9]+)', output)
        if match:
            temperature_list.append(float(match.group(1)))
            humidity_list.append(float(match.group(2)))
        else:
            time.sleep(3)

    humidity = round(sum(humidity_list) / len(humidity_list), 1) 
    temperature = sum(temperature_list) / len(temperature_list)     
    # Convert temp from C to F
    fahrenheit = round(temperature*1.8+32, 1)
    
    return fahrenheit, humidity


def fan(fahrenheit):
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
    cold_outside = [1,2,3,4,10,11,12]
    hot_outside = [5,6,7,8,9]
    outside_temperature = get_outdoor_temperature()
    outside_temperature = int(outside_temperature[0])
    
    current_date = get_date_and_time()[0]
    current_date = current_date.split('/')
    current_month = int(current_date[0])

    if outside_temperature < 55:
        # then heat will be needed
        current_air_value = 'hot'
        if fahrenheit < desired_temp:
            GPIO.output(fan, False)
            fan_action = 'ON'
        elif fahrenheit > desired_temp:
            GPIO.output(fan, True)
            fan_action = 'OFF'

    if outside_temperature > 65:
        # then air conditioning will be needed
        current_air_value = 'cold'
        if fahrenheit > desired_temp:
            GPIO.output(fan, False)
            fan_action = 'ON'
        elif fahrenheit < desired_temp:
            GPIO.output(fan, True)
            fan_action = 'OFF'

    print fan_action
    return current_air_value
    """
    *** NEED TO ADD TEST TO SEE IF HEAT OR AC IS ON
    """

def lights(motion, motion_detected_time):
    # sets the lights on or off depending on motion being detected in the room
    light_delay = 1             # number of minutes to wait until the lights shut off
    global false_time_list      # references the global list to keep track of latest false motion time
    # Turns lights on when motion is detected
    if motion == True:
        # NOTE!! For some reason when the relay is told False it's actually turns on
        # For some reason the boolean logic is reversed when dealing with the relay
        GPIO.output(light_bank_1, False)
        GPIO.output(light_bank_2, False)
        GPIO.output(light_bank_3, False)
        # resets the list of times for false list
        false_time_list = []

    elif motion == False:
        # Converts current time into number of minutes 20:15 --> 1215 minutes
        current_time = get_date_and_time()[1]
        current_time = current_time.split(':')
        current_time = (int(current_time[0]) * 60) + int(current_time[1])
        # Converts time when motion was detected into number of minutes 20:15 --> 1215 minutes        
        motion_detected_time = motion_detected_time.split(':')
        motion_detected_time = (int(motion_detected_time[0]) * 60) + int(motion_detected_time[1])
        # appends the time in minutes (20:15 --> 1215 minutes) to the global list false_time_list
        false_time_list.append(motion_detected_time)
        false_time = min(false_time_list)

        # keeps false_time_list from getting infinately huge and limits it to 5 entries
        # if the length exceeds 5 then the list is reset and adds the lowest time into
        # the new list
        if len(false_time_list) > 5:
            false_time_list = [false_time]
        elapsed_time = abs(false_time - current_time)
        # where light delay is evaluated against the lowest time, which determines if the lights should be
        # shut off or not
        if elapsed_time >= light_delay:
            # NOTE!! For some reason when the relay is told False it's actually turns on
            # For some reason the boolean logic is reversed when dealing with the relay
            GPIO.output(light_bank_1, True)
            GPIO.output(light_bank_2, True)
            GPIO.output(light_bank_3, True)


def get_motion():
    # Gets the motion in the room as a boolean
    # If there is motion then return True and return current time
    motion = GPIO.input(motion_sensor)
    if motion == 0:
        motion = False

    if motion == 1:
        motion = True
    
    motion_detected_time = get_date_and_time()
    motion_detected_time = motion_detected_time[1]

    return motion, motion_detected_time

def get_outdoor_temperature():
    """
    will be used later on using mechanize 
    Generates a web browser instance 
    Opens http://www.weather.com/ and submits Olivet, MI as the location
    and then scrapes the current outside temperature off the website and
    returns that temperature to the main loop for use else where in the
    program
    """
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
    """
    Gets the date and time and then returns those values as the tuple: ([2/10/2014], [15:30])
    """
    current_date_and_time = datetime.datetime.now()
    month = str(current_date_and_time.month)
    day = str(current_date_and_time.day)
    year = str(current_date_and_time.year)
    hour = str(current_date_and_time.hour)
    minute = str(current_date_and_time.minute)

    date = month+'/' + day+'/' + year
    time = hour+':' + minute
    return date, time

def get_external_ip():
    """
    Generates a web browser instance 
    Opens www.whatsmyip.com/ and then scrapes your current external ip adress
    """
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
    html = br.open('http://www.whatismyip.com/')
    html = html.read()
    html = unicode(html, errors='ignore')

    # Searches through the raw html file and grabs the paragraph "the-ip", where the external IP is displayed 
    match = re.search('<div class="the-ip">(.*)</div>', html)
    # Looks at "the-ip" section and finds html char, i.e. '&#58' 
    if match:
        chars = re.findall('\&\#(\d*)', match.group(1))
        external_ip = ''.join([chr(int(char)) for char in chars])
        return external_ip


def post_to_google_spreadsheet(date, time, fahrenheit, humidity, motion):

    """ 
    *** STILL NEEDS TO BE DONE ***

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
        

if __name__ == "__main__": main()