#!/usr/bin/env python

# Transform our log file so we have a row for each 15 minute increment of
# the day, and a column for each day

import sys

# Load the data
log_data = open(sys.argv[1], 'r')

# Create an array to hold the data
data = []

# Figure out how many days we need to store
days = []

for line in log_data:
    date = line.split(",")[0].split(" ")[0]
    if len(days) == 0 or days[len(days) - 1] != date:
        days.append(date)

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

log_data.seek(0,0)

# Read each line into an array
row = 0
col = 0
for line in log_data:
    if line.split(",")[0].split(" ")[0] != "report_datetime":
        date = line.split(",")[0].split(" ")[0]
        time = line.split(",")[0].split(" ")[1][:-3]
        row = days.index(date)
        col = data[0].index(time)
        data[row][col] = int(line.split(",")[2])

# Write array to a file
file = open(sys.argv[2], 'w')
for line in data:
    for column in line:
        file.write(str(column))
        file.write("\t")
    file.write("\n")
file.close()