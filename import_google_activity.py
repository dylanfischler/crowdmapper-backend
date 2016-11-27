#!/usr/bin/env python

import sys
import json
from LocationWriter import LocationWriter
import ConfigParser
import math

locationList = []

def processActivityFile(activityPath, locationWriter):
    with open(activityPath) as file:
        data = json.load(file)
        locations = data.get('locations')
        for location in locations:
            locationWriter.writeLocation(createLocationDict(location))

        locationWriter.commitWrites()

def createLocationDict(locationObj):
    pow = -7.0
    return {
        "lat": locationObj.get("latitudeE7") * math.pow(10, pow),
        "long": locationObj.get("longitudeE7") * math.pow(10, pow),
        "timestamp": locationObj.get("timestampMs")
    }

if len(sys.argv) < 2:
    print("Error: Must provide activity JSON as argument to function")
    print("{} ACTIVITY_FILE.json".format(sys.argv[0]))
else:
    config = ConfigParser.RawConfigParser()
    config.read('db_config')
    configSections = config._sections
    locationWriter = None

    if 'db' in configSections:
        db_config = configSections.get('db')
        db_config.pop('__name__', None)
        locationWriter = LocationWriter(db_config)
        locationWriter.connectToDatabase()
        processActivityFile(sys.argv[1], locationWriter)
    else:
        print("No db section in config")