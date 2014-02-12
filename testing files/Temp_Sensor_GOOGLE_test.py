import gspread

def main():
    date = 'date'
    time = 'time'
    fahrenheit = 24
    humidity = 15
    motion = True

    post_to_google_spreadsheet(date, time, fahrenheit, humidity, motion)


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


    user_info = open('/Users/jaredrluellen/Google Drive/Raspberry Pi/RasPiHeatLight/user_info.txt', 'r')
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


            


        #worksheet.append_row(date, time, fahrenheit, humidity, motion)
    except:
        print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
        
if __name__ == "__main__": main()