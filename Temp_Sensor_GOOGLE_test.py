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
password    = linestring = open('password.txt', 'r').read()
spreadsheet = 'Computer Science Lab Temperature'



"""






"""

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
while val > 2:
  
  
  temp = 75
  humidity = 25
  now = datetime.datetime.now()

  date =  datetime.date.today().strftime("%m %d %Y")
  current_time = time.strftime( "%H:%M:%S")
  motion = True 

  try:
    values = [date,current_time, temp, humidity, motion]
    

    worksheet.update_cell(val, 1, date)
    worksheet.update_cell(val, 2, current_time)
    worksheet.update_cell(val, 3, temp)
    worksheet.update_cell(val, 4, humidity)
    worksheet.update_cell(val, 5, motion)

    worksheet.update_cell(2, 10, val)




    
  except:
    print "Unable to append data.  Check your connection?"
    sys.exit()

  # Wait 30 seconds before continuing
  print "Wrote a row to %s" % spreadsheet
  time.sleep(0)
  val += 1
  print val
  