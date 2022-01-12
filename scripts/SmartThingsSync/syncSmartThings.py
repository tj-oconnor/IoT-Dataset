from bs4 import BeautifulSoup
import requests
import json
import re
import os
import datetime
from config import devices, searchByDeviceUuid
cookies = {'JSESSIONID': 'pleaseretrievefrombrowsersession'}
events = {}
endpoint = "https://graph-na04-useast2.api.smartthings.com/event/listMoreEvents"
s = requests.Session()
s.cookies.update(cookies)
def parseEvents(html, end=None):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')
    loadedEvents = []
    for row in rows:
        columns = row.find_all('td')
        # parse out date.
        event = {}
        event["date"] = columns[0].text.split('\n')[3].strip()
        event["uuid"] = columns[0].find("a")["href"].split("event/")[1].split("?")[0]
        if not (end is None):
            if event["uuid"] == end:
                return (loadedEvents, True) # end early
        event["event_type"] = columns[3].text.strip()
        event["event_value"] = columns[4].text.strip()
        #print("{} -> {}".format(event_type, event_value))
        loadedEvents.append(event)
    return (loadedEvents, False)
oldDevices = {}
def retrieveEvents(device, endUuid=None):
    records = 1
    lastUuid = None
    allEvents = []
    while records > 0:
        url = endpoint + "?id={}&type=device&max=200".format(device)
        if not (lastUuid is None):
            url += "&startAfter=" + lastUuid
        r = s.get(url)
        try:
            data = json.loads(r.text)
            records = data["fetchedEventSize"]
            htmldata = data["renderedEvents"]
            newEvents, earlyEnd = (parseEvents(htmldata, endUuid), parseEvents(htmldata))[endUuid is None]
            allEvents += newEvents
            if earlyEnd:
                return allEvents
            lastUuid = allEvents[-1]["uuid"]
        except:
            print("Some error occurred fetching data. (maybe token?)")
            break
    return allEvents

total = 0
DateFormat =  "%Y-%m-%d %I:%M:%S.%f %p %Z"
def loadOldUuids():
    with open('./smartthings-events.json', 'r') as oldEvents:
        oEvents = oldEvents.readlines()
        for event in oEvents:
            obj = json.loads(event)
            if not obj["device"] in oldDevices:
                print("Discovered old entries for device {} ({}), adding tracker.".format(obj["device"], searchByDeviceUuid(obj["device"])["name"]))
                oldDevices[obj["device"]] = obj
            else:
                dateNew = datetime.datetime.strptime(obj["date"],DateFormat)
                dateOld = datetime.datetime.strptime(oldDevices[obj["device"]]["date"], DateFormat)
                if (dateNew > dateOld):
                    oldDevices[obj["device"]] = obj

if (os.path.exists("./smartthings-events.json")):
    loadOldUuids()
for device in devices:
    deviceName = device["name"]
    if (device["uuid"] in oldDevices):
        print("Syncing up to event {} for device {}".format(oldDevices[device["uuid"]]["uuid"], deviceName))
        events[deviceName] = retrieveEvents(device["uuid"], oldDevices[device["uuid"]]["uuid"])
        amt = len(events[deviceName])
        print("Retrieved {} new events for device {}".format(amt, device["name"]))
    else:
        print("Syncing all events for {}".format(deviceName))
        events[deviceName] = retrieveEvents(device["uuid"])
    total += amt
with open('./smartthings-events.json', 'a') as eventFile:
    for device in devices:
        for event in reversed(events[device["name"]]): # oldest events should be first(ish)
            event["device"] = device["uuid"]
            writer = eventFile.writelines(json.dumps(event) + "\n")
