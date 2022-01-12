from config import devices, searchByDeviceUuid
import json
import datetime

mappings = {
    "temperature": "event_temp",
    "motion": {
        "active": "event_motionstart",
        "inactive": "event_motionend"
    },
    "rssi": "event_rssi",
    "lqi": "event_lqi",
    "switch": {
        "off": "event_off",
        "on": "event_on"
    },
    "sound": {
        "detected": "event_soundstart",
        "not detected": "event_soundend",
    },
    "water": {
        "dry": "event_waterend",
        "wet": "event_waterstart"
    },
    "lock": {
        "locked": "event_lock",
        "unlocked with": "event_timeoutunlock",
        "unlocked": "event_unlock",
 
    },
    "detected": {
        '{\"data\":{\"qty\":0}': "event_personend",
        '{\"data\":{\"qty\":1}': "event_personstart"
    },
    "contact": {
        "closed": "event_close",
        "open": "event_open"
    },
    "clip": "event_record",
    "acceleration": "event_move"
}


def convertDate(date):
    dateobj = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M:%S.%f %p %Z")
    return dateobj.strftime("%B %d, %Y at %I:%M:%S%p")
totalLines = 0
totalOutputs = 0
StartDate = datetime.datetime.strptime("2021-03-08 09:30:00.000 AM EST", "%Y-%m-%d %I:%M:%S.%f %p %Z")
EndDate = datetime.datetime.strptime("2021-03-15 05:16:00.000 PM EST", "%Y-%m-%d %I:%M:%S.%f %p %Z")
with open('smartthings-events.json', 'r') as fp:
    with open('../smartthings-events.csv', 'w') as wp:
        lines = fp.readlines()
        for line in lines:
            totalLines += 1
            obj = json.loads(line)
            date = datetime.datetime.strptime(obj["date"], "%Y-%m-%d %I:%M:%S.%f %p %Z")
            if (date < StartDate or date > EndDate):
                continue
            if not obj["event_type"] in mappings:
                print("Unknown event", obj["event_type"])
                continue
            mapping = mappings[obj["event_type"]]
            if isinstance(mapping, dict):
                for v in mapping.keys():
                    if obj["event_value"].startswith(v):
                        wp.write('"{}","{}","{}"\n'.format(convertDate(obj["date"]), searchByDeviceUuid(obj["device"])["name"], mapping[v]))
                        totalOutputs += 1
                        break
            else:
                wp.write('"{}","{}","{}"\n'.format(convertDate(obj["date"]), searchByDeviceUuid(obj["device"])["name"], mapping))
                totalOutputs += 1

print("{} lines, {} csv outputs".format(totalLines, totalOutputs))
            
