#!/usr/bin/env python

# Transform our log file so we have a row for each 15 minute increment of
# the day, and a column for each day

import sys
# This is so the script will work on my shared server
sys.path.append('/usr/home/jreardon/scripts/python-dateutil-2.6.0')
from datetime import datetime
from dateutil import tz

def find_datetime(date_time, dataset):
    for i, line in enumerate(dataset):
        if date_time == line[0]:
            return i

def convert_utc_to_local(utc_date_time):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    utc = datetime.strptime(utc_date_time, '%Y-%m-%d %H:%M:%S')

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    local_date_time = utc.astimezone(to_zone)

    # Convert it to a string in a format we expect
    local_date_time_str = local_date_time.strftime('%Y-%m-%d %H:%M:%S')

    return local_date_time_str

# Output format
TIME_ROWS = False
if sys.argv[3] == "1":
    TIME_ROWS = True

# Load the data
log_data = open(sys.argv[1], 'r')

# Create an array to hold the data
data = []

# Figure out how many days we need to store
days = []

for line in log_data:
    date = line.split(",")[0]
    if date != "report_datetime":
        date = convert_utc_to_local(date).split(" ")[0]
    if len(days) == 0 or days[len(days) - 1] != date:
        days.append(date)

# Create the array (with dates as rows)
if TIME_ROWS != True:

    for day in days:
        datarow = [day]
        for hour in range(24):
            if day == "report_datetime":
                # First row is a header
                datarow.append(str(hour).zfill(2) + ":00")
                datarow.append(str(hour).zfill(2) + ":15")
                datarow.append(str(hour).zfill(2) + ":30")
                datarow.append(str(hour).zfill(2) + ":45")
            else:
                # Fill the rest of the array with zeros
                for quarter in range(4):
                    datarow.append(0)
        data.append(datarow)

# Create the array (with times as rows)
if TIME_ROWS:

    # First row
    datarow = []
    for day in days:
        datarow.append(day)

    data.append(datarow)

    # First column is a time, the rest should be zeros
    # Lots of repitition here, sad!
    for hour in range(24):
        for hourpart in range(4):
            if hourpart == 0:
                datarow = [str(hour).zfill(2) + ":00"]
                for day in days:
                    if day != "report_datetime":
                        datarow.append("0")
            if hourpart == 1:
                datarow = [str(hour).zfill(2) + ":15"]
                for day in days:
                    if day != "report_datetime":
                        datarow.append("0")
            if hourpart == 2:
                datarow = [str(hour).zfill(2) + ":30"]
                for day in days:
                    if day != "report_datetime":
                        datarow.append("0")
            if hourpart == 3:
                datarow = [str(hour).zfill(2) + ":45"]
                for day in days:
                    if day != "report_datetime":
                        datarow.append("0")
            data.append(datarow)

log_data.seek(0,0)

# Read each line into an array
row = 0
col = 0
for line in log_data:
    if line.split(",")[0].split(" ")[0] != "report_datetime":
        localtime = str(convert_utc_to_local(line.split(",")[0]))
        date = localtime.split(" ")[0]
        time = localtime.split(" ")[1][:-3]
        if TIME_ROWS:
            row = find_datetime(time, data)
            col = data[0].index(date)
        else:
            row = days.index(date)
            col = data[0].index(time)
        data[row][col] = line.split(",")[2].strip()

# Write array to a file
file = open(sys.argv[2], 'w')
for line in data:
    for column in line:
        file.write(str(column))
        file.write("\t")
    file.write("\b\n")
file.close()
