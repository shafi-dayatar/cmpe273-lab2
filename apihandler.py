import json
import requests
from datetime import datetime
import operator

def call(lat, lon, radius):
    url = "https://api.spotcrime.com/crimes.json"
    payload = (("lat", lat), ("lon", lon), ("radius",radius),("key","."))
    response = requests.get(url, params=payload)    
    data = response.json()
    response = crimeParser(data["crimes"])
    return response

def crimeTimeCount(crimeTime, cr_time):
    crimeHappenedOn = datetime.strptime(cr_time, "%m/%d/%y %I:%M %p")
    if crimeHappenedOn.hour >= 0 and crimeHappenedOn.hour < 3:
        crimeTime["12:01am-3am"] += 1
    elif crimeHappenedOn.hour >= 3 and crimeHappenedOn.hour < 6:
        crimeTime["3:01am-6am"] += 1
    elif crimeHappenedOn.hour >= 6 and crimeHappenedOn.hour < 9:
        crimeTime["6:01am-9am"] += 1
    elif crimeHappenedOn.hour >= 9 and crimeHappenedOn.hour <12:
        crimeTime["9:01am-12noon"] += 1
    elif crimeHappenedOn.hour >= 12 and crimeHappenedOn.hour <15:
        crimeTime["12:01pm-3pm"] += 1
    elif crimeHappenedOn.hour >= 15 and crimeHappenedOn.hour <18:
        crimeTime["3:01pm-6pm"] += 1
    elif crimeHappenedOn.hour >= 18 and crimeHappenedOn.hour <21:
        crimeTime["6:01pm-9pm"] += 1
    else:
        crimeTime["9:01pm-12midnight"] += 1
    return crimeTime

def crimeTypeCount(crimeType, cr_type):
    crimeType[cr_type] = crimeType.get(cr_type, 0) + 1
    return crimeType

def streetCrimeLookup(streetName, address):
    street = address
    if (" OF " in address):
      street = address.split(" OF ")[1]
      streetName[street] = streetName.get(street, 0) + 1
    elif (" & " in address):
      street1, street2 = address.split(" & ")
      streetName[street1] = streetName.get(street1, 0) + 1
      streetName[street2] = streetName.get(street2, 0) + 1
    else:
      streetName[address] = streetName.get(address, 0) + 1
    return streetName

def topThreeCrimeSteets(streetName):
    final_streets =[]
    streetName = sorted(streetName.items(), key=operator.itemgetter(1))
    for streets in streetName[len(streetName)-3:len(streetName)]:
        final_streets.append(streets[0])
    return final_streets

def crimeParser(crimes):
    response = {}
    crimeType = {}
    streetName = {}
    crimeTime = { "12:01am-3am" : 0, "3:01am-6am" : 0, "6:01am-9am" : 0, "9:01am-12noon" : 0,
        "12:01pm-3pm" : 0, "3:01pm-6pm" : 0, "6:01pm-9pm" : 0, "9:01pm-12midnight" : 0}
    response["total_crime"] = len(crimes)
    for crime in crimes:
        crimeType = crimeTypeCount(crimeType, crime["type"])
        crimeTime = crimeTimeCount(crimeTime, crime["date"])
        streetName = streetCrimeLookup(streetName, crime["address"])

    response["crime_type_count"] = crimeType
    response["event_time_count"] = crimeTime
    response["the_most_dangerous_streets"] = topThreeCrimeSteets(streetName)


    print response
    return response