import gspread
import re

user_info = open('../user_info.txt', 'r')
print user_info
user_name = user_info.readline()
user_pass = user_info.readline()
spreadsheet = 'Computer Science Lab Temperature'
user_info.close()

# Login with your Google account
try:
    gc = gspread.login(user_name, user_pass)
    print "Attempting to Login"
    workbook = gc.open(spreadsheet)
    sheet = workbook.worksheets()
    list_of_sheets = []
    for i in sheet:
        i = str(i)
        sheets = re.search('<Worksheet \'(.*)\' ',i)
        list_of_sheets.append(sheets.group(1))
        print list_of_sheets

    print 'getting list of worksheets'
except:
    print "Unable to log in.  Check your email address/password"
    

# Open a worksheet from your spreadsheet using the filename
occupant_status = 'Exit Log'

if occupant_status in list_of_sheets:
    active_worksheet = workbook.worksheet(occupant_status)
    active_worksheet.update_acell('A1', 'Working')
    print 'entry succeeded'

    # worksheet = gc.worksheet(0)

    # Alternatively, open a spreadsheet using the spreadsheet's key
    # worksheet = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
    # A1 = worksheet.acell('A1')
    
    # worksheet.append_row(date)
    # data_set = ["data"]
    # worksheet.add_rows(1)
    # row = str(worksheet.row_count)
    # columns = "ABCDEFG"
    # for col, datum in enumerate(data_set):
    #     worksheet.update_acell(columns[col] + row, datum)
