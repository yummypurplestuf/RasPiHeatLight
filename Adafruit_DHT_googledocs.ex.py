#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import gspread
import os

# ===========================================================================
# Google Account Details
# ===========================================================================

# Account details for google docs
email       = 'jared.luellen@cs.olivetcollege.edu'
password    = subprocess.check_output(["echo", "$MY_PASSWORD"]);
spreadsheet = 'Computer Science Lab Temperature'

# To add MY_PASSWORD on a local machine edit .bashrc and append at the bottom MY_PASSWORD="password"
# Then to set that as your password, run the .bashrc like (. .bashrc) <---enter this in terminal without the parens
# That way you password doesn't live in the code and is controlled by the machine you're executing from :)

# ===========================================================================
# Example Code
# ===========================================================================


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

# Continuously append data
while(True):
  # Run the DHT program to get the humidity and temperature readings!

  output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
  print output
  matches = re.search("Temp =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  temp = float(matches.group(1))
  
  # search for humidity printout
  matches = re.search("Hum =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  humidity = float(matches.group(1))

  print "Temperature: %.1f C" % temp
  print "Humidity:    %.1f %%" % humidity
 
  # Append the data in the spreadsheet, including a timestamp
  try:
    values = [datetime.datetime.now(), temp, humidity]
    worksheet.append_row(values)
  except:
    print "Unable to append data.  Check your connection?"
    sys.exit()

  # Wait 30 seconds before continuing
  print "Wrote a row to %s" % spreadsheet
  time.sleep(30)
