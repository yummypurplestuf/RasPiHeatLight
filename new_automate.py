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
# 1 hp = 745.699872w, 1/6hp motor = 124.9499w, 124.9499w/120v = 1.04A
#########################################################################


import time
import RPi.GPIO as GPIO
import subprocess
import re
import sys
import datetime
import gspread
import mechanize



fan_motor = 25                      # Pin 1 on 4-Channel Relay
light_bank_1 = 24                   # Pin 2 on 4-Channel Relay
light_bank_2 = 8                    # Pin 3 on 4-Channel Relay
light_bank_3 = 23                   # Pin 4 on 4-Channel Relay
motion_sensor = 11                  # Pin for Motion Sensor Input
temp = 4                            # Pin for Temperature/Humidity Sensor
desired_temp = 75                   # The temperature you would like it to be           
light_delay = 1 
temp_sensor_delay = 3
outside_temperature_delay = 10

false_time_list = []
outside_temperature_list = []
temperature_sensor_delay_list = []
###################################################################################

GPIO.setwarnings(False)         
GPIO.setmode(GPIO.BCM)              # GPIO Board init

GPIO.setup(fan_motor, GPIO.OUT)           # Inits the relay connected to the fan
GPIO.setup(light_bank_1, GPIO.OUT)  # "         "
GPIO.setup(light_bank_2, GPIO.OUT)  # "         "
GPIO.setup(light_bank_3, GPIO.OUT)  # "         "
GPIO.setup(motion_sensor, GPIO.IN)  # Inits the Motion Sensor pin
GPIO.setup(temp, GPIO.IN)           # Inits the Temperature Sensor pin

"""
NEED TO WRITE A TIMING FUNCTION TO HANDLE ALL OF THE TIMING OF LIGHTS, TEMP, FAN AND get_outdoor_temperature
"""


def main():
    
    while True:
        try:    
            motion = get_motion()
            motion_detected_time_in_minutes = motion[1]
            motion = motion[0]
            temperature = get_temp_and_humidity()
            fahrenheit = temperature_sensor_delay_list[1]
            humidity = temperature_sensor_delay_list[2]
            fan_status = fan(fahrenheit)
            outside_temperature = get_outdoor_temperature()
                
            light_status = lights(motion)

            # print_status(motion, motion_detected_time_in_minutes, light_status, fan_status, fahrenheit, humidity, outside_temperature)
            # post_to_google_spreadsheet(date, time, fahrenheit, humidity, motion)
        
        except:
            sys_exit_commands()
            sys.exit()

def print_status(motion, motion_detected_time_in_minutes, light_status, fan_status, fahrenheit, humidity, outside_temperature):
        print '     '
        print "Motion is: " + str(motion) + ' ' + str(motion_detected_time_in_minutes)
        print "Light Status: " + str(light_status)
        print "Fan Status: " + str(fan_status)
        print "Temperature Stats: " + str(fahrenheit) + ' ' + str(humidity)
        print "Outside Temperature: " + str(outside_temperature)
        time.sleep(1)

def sys_exit_commands():
    # turns off all lights and fan when something has failed in the program
    GPIO.output(fan_motor, True)
    GPIO.output(light_bank_1, True)
    GPIO.output(light_bank_2, True)
    GPIO.output(light_bank_3, True)
    
def get_temp_and_humidity():
    """
    Runs a C file that interacts with the DHT11 sensor, matches the temperature and humidity
        off of the standard output from the program and then adds those values to seperate list
        so that the temperature and humidity values can be averaged out in order to get more 
        accurate values.
    """
    temperature_list = []
    humidity_list = []
    
    global temp_sensor_delay
    global temperature_sensor_delay_list
    current_time = get_date_and_time()[2]
    
    if len(temperature_sensor_delay_list) ==0:
        temperature_sensor_delay_list.append(current_time)
        temperature_sensor_delay_list[0] = temperature_sensor_delay_list[0] + temp_sensor_delay + 1
        run_temp_sensor = True

    last_added_time = temperature_sensor_delay_list[0]
    elapsed_time = abs(last_added_time - current_time)

    if elapsed_time < temp_sensor_delay:
        if len(temperature_sensor_delay_list) == 3:
            fahrenheit = temperature_sensor_delay_list[1]
            humidity = temperature_sensor_delay_list [2]
            return fahrenheit, humidity
            run_temp_sensor = False

    if elapsed_time >= temp_sensor_delay:
        run_temp_sensor = True
    
    if run_temp_sensor == True:
        # Run the DHT program to get the humidity and temperature readings!
        output = subprocess.check_output(["./Adafruit_DHT", "11", "4"])
        match = re.search('Temp = ([0-9]+) \*C, Hum = ([0-9]+)', output)
        if match:
            temperature_list.append(float(match.group(1)))
            humidity_list.append(float(match.group(2)))
            humidity = round(sum(humidity_list) / len(humidity_list), 1) 
            temperature = sum(temperature_list) / len(temperature_list)     
            # Convert temp from C to F
            fahrenheit = round(temperature*1.8+32, 1)

            if len(temperature_sensor_delay_list) != 3:
                temperature_sensor_delay_list[0] = get_date_and_time()[2]
                temperature_sensor_delay_list.append(fahrenheit)
                temperature_sensor_delay_list.append(humidity)
                
            
            elif len(temperature_sensor_delay_list) == 3:
                print current_time
                temperature_sensor_delay_list[0] = current_time
                temperature_sensor_delay_list[1] = fahrenheit
                temperature_sensor_delay_list[2] = humidity

        else:
            time.sleep(3)

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
    cold_outside = [1,2,3,11,12]
    hot_outside = [6,7,8,9]
    easy_months = cold_outside + hot_outside
    current_date = get_date_and_time()[0]
    current_date = current_date.split('/')
    current_month = int(current_date[0])
    if current_month in cold_outside:
        # then heat will be needed
        current_air_value = 'hot'
        if fahrenheit < desired_temp:
            GPIO.output(fan_motor, False)
            fan_status = 'ON'
        elif fahrenheit > desired_temp:
            GPIO.output(fan_motor, True)
            fan_status = 'OFF'

    elif current_month in hot_outside:
        # then air conditioning will be needed
        current_air_value = 'cold'
        if fahrenheit > desired_temp:
            GPIO.output(fan_motor, False)
            fan_status = 'ON'
        elif fahrenheit < desired_temp:
            GPIO.output(fan_motor, True)
            fan_status = 'OFF'
    
    elif current_month not in easy_months:
        # if the current month is not obvious then check www.weather.com
        # and compare the temperature accordingly
        outside_temperature = get_outdoor_temperature()
        outside_temperature = int(outside_temperature[0])

        if outside_temperature > 65:
            # Means this is spring or warmer weather
            current_air_value = 'hot'
            if fahrenheit < desired_temp:
                GPIO.output(fan_motor, False)
                fan_status = 'ON'
            elif fahrenheit > desired_temp:
                GPIO.output(fan_motor, True)
                fan_status = 'OFF'
            else:
                GPIO.output(fan_motor, True)
                fan_status = 'OFF'

        if outside_temperature < 65:
            # means it is winter or colder weather
            current_air_value = 'cold'
            if fahrenheit < desired_temp:
                GPIO.output(fan_motor, False)
                fan_status = 'ON'
            elif fahrenheit > desired_temp:
                GPIO.output(fan_motor, True)
                fan_status = 'OFF'
            else:
                GPIO.output(fan_motor, True)
                fan_status = 'OFF'

    return fan_status, current_air_value
    """
    *** NEED TO ADD TEST TO SEE IF HEAT OR AC IS ON
    """

def lights(motion):
    # sets the lights on or off depending on motion being detected in the room
    global light_delay            # number of minutes to wait until the lights shut off
    global false_time_list
    # Turns lights on when motion is detected
    if motion == True:
        # NOTE!! For some reason when the relay is told False it's actually turns on
        # For some reason the boolean logic is reversed when dealing with the relay
        GPIO.output(light_bank_1, False)
        GPIO.output(light_bank_2, False)
        GPIO.output(light_bank_3, False)
        # resets the list of times for false list
        false_time_list = []
        light_status = True

    elif motion == False:
        if len(false_time_list) == 0:
            current_time = get_date_and_time()[2]
            false_time_list.append(current_time)

        if len(false_time_list) !=0:

            current_time = get_date_and_time()[2]
            false_time = false_time_list[0]
            elapsed_time = abs(false_time - current_time)
            light_status = True
            # where light delay is evaluated against the lowest time, which determines if the lights should be
            # shut off or not
            if elapsed_time >= light_delay:
                # NOTE!! For some reason when the relay is told False it's actually turns on
                # For some reason the boolean logic is reversed when dealing with the relay
                GPIO.output(light_bank_1, True)
                GPIO.output(light_bank_2, True)
                GPIO.output(light_bank_3, True)
                light_status = False

    return light_status


def get_motion():
    # Gets the motion in the room as a boolean
    # If there is motion then return True and return current time
    motion = GPIO.input(motion_sensor)
    if motion == 0:
        motion = False

    if motion == 1:
        motion = True
    
    motion_detected_time_in_minutes = get_date_and_time()[2]
    return motion, motion_detected_time_in_minutes

def get_outdoor_temperature():
    """
    will be used later on using mechanize 
    Generates a web browser instance 
    Opens http://www.weather.com/ and submits Olivet, MI as the location
    and then scrapes the current outside temperature off the website and
    returns that temperature to the main loop for use else where in the
    program
    """
    # refers to the global outside_temperature_list
    global outside_temperature_list
    # sets threshold for when to check the outside temperature and when not too
    global outside_temperature_delay
    # grabs current time in minutes
    current_time = get_date_and_time()[2]
    
    if len(outside_temperature_list) == 0:
        outside_temperature_list.append(current_time + outside_temperature_delay + 1)

    # grabs the time of the last added temperature
    last_added = outside_temperature_list[0]
    # finds elapsed time from last added and the current time
    elapsed_time = abs(last_added - current_time)


    # if elapsed time is less then preset ammount then get last temp added and return that value
    if elapsed_time <= outside_temperature_delay:
        last_temp = outside_temperature_list[-1]
        return last_temp

    # if elapsed time is greater than the delay then get a new outside temperature
    if elapsed_time > outside_temperature_delay:
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
        # selects form on page and inputs location into form
        br.select_form(nr=0)
        # input location in search box
        br['where'] = "Olivet, MI"
        html = br.submit()
        html = html.read()

        outside_list = []
        # matches temperature and unit, then append it to a list
        match = re.search('<span itemprop="temperature-fahrenheit">(\d*)</span>', html)
        outside_list.append(int(match.group(1)))
        match = re.search('<span class="wx-unit">(.)</span>', html) 
        outside_list.append(u'\xb0'.encode("UTF-8") + match.group(1))
        
        # gets current outside temperature and sets it to a variable    
        current_outside_temperature = outside_list[0]

        if current_outside_temperature not in outside_temperature_list:
            # gets current time in minutes
            last_checked = get_date_and_time()[2]
            # adds current time in minutes to outside_temperature_list[0]
            outside_temperature_list[0] = last_checked
            # appends current temperature to outside_temperature_list
            outside_temperature_list.append(current_outside_temperature)
            return current_outside_temperature


    if len(outside_temperature_list) > 10:
        last_checked = outside_temperature_list[0]
        lowest_temp_val = min(outside_temperature_list[1:])
        outside_temperature_list = [last_checked, lowest_temp_val]


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

    # Converts current time into number of minutes 20:15 --> 1215 minutes
    time_in_minutes = time.split(':')
    time_in_minutes = (int(time_in_minutes[0]) * 60) + int(time_in_minutes[1])

    return date, time, time_in_minutes

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
        # A1 = worksheet.acell('A1')
        
        # worksheet.append_row(date)
        data_set = [date, time, fahrenheit, humidity, motion]
        worksheet.add_rows(1)
        row = str(worksheet.row_count)
        columns = "ABCDEFG"
        for col, datum in enumerate(data_set):
            worksheet.update_acell(columns[col] + row, datum)
    except:
        print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
        

if __name__ == "__main__": main()