#!/usr/bin/env python

# We just need to grab a bit of historical data to get started...
# Pass the name of the output file as the first argument

import sys
import urllib
import json
from time import gmtime, strftime

# Get the station status file (https://gbfs.citibikenyc.com/gbfs/en/station_status.json)
status = urllib.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_status.json").read()

# Parse into something we can work with
status_dict = json.loads(status)

# For station 3416, output all of the fields to a line in a text file
for station in status_dict['data']['stations']:
    if station['station_id'] == '3416':
        log_file = open(sys.argv[1], 'a')
        log_file.write (str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + ', '
                        + str(station['station_id']) + ', '
                        + str(station['num_bikes_available']) + ', '
                        + str(station['num_bikes_disabled']) + ', '
                        + str(station['num_docks_available']) + ', '
                        + str(station['num_docks_disabled']) + ', '
                        + str(station['is_installed']) + ', '
                        + str(station['is_renting']) + ', '
                        + str(station['is_returning']) + ', '
                        + str(station['last_reported'])
                        + '\n')
        log_file.close()

# TODO: Capture all stations for later loading and analysis