import datetime
import time


def main():
    current = get_date_and_time()
    time.sleep(120)    
    later = get_date_and_time()

    if current[1] != later[1]:
        print False, current, later
    else:
        print True

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

if __name__ == "__main__": main()