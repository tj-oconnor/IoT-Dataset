import datetime

# device ->
# - time: event
actions = {
    "yale-lock-01": {
        "30": "event_unlock",
        "15": "event_lock"
    },
    "hue-light-05": {
        "00": "event_on",
        "45": "event_off"
    },
    "hue-light-01": {
        "00": "event_on",
        "15": "event_off"
    },
    "hue-light-02": {
        "00": "event_on",
        "15": "event_off"
    },
    "hue-light-03": {
        "00": "event_on",
        "30": "event_off"
    },
    "hue-light-04": {
        "00": "event_on",
        "30": "event_off"
    },
    "smartthings-outlet-01": {
        "45": "event_off",
        "00": "event_on"
    },
    "ultraloq-lock-01": {
        "30": "event_unlock",
        "15": "event_lock"
    },
    "blink-hub-01": {
        "30": "event_disarm",
        "15": "event_arm"
    },
    "wyze-cam-01": {
        "45": "event_off",
        "30": "event_restart",
        "15": "event_record",
        "00": "event_on"
    },
    "kasa-cam-01": {
        "45": "event_off",
        "00": "event_on"
    },
    "arlo-hub-01": {
        "30": "event_disarm",
        "15": "event_arm"
    },
    "arlo-cam-02": {
        "45": "event_record"
    },
    "arlo-cam-01": {
        "00": "event_record"
    }
}

# pull dateTime object from string, used to filter IFTTT events and android events
def parseDate(dateStr):
    dateFormats = ["%B %d, %Y at %I:%M:%S%p",
                    "%B %d, %Y at %I:%M%p"
    ]
    for dF in dateFormats:
        try:
            date_time_obj = datetime.datetime.strptime(dateStr, dF)
            return date_time_obj
        except:
            ValueError
            pass
    return None

def printDate(dateobj):
    return dateobj.strftime("%B %d, %Y at %I:%M%p")
# when to start counting
StartTime = parseDate("March 08, 2021 at 09:30AM")
EndTime = parseDate("March 15, 2021 at 05:16PM")
with open("ifttt-actions.csv", "w") as fp:
    CurTime = StartTime
    while CurTime < EndTime:
        TargetMinute = "{0:02d}".format(CurTime.minute)
        for device in actions:
            if TargetMinute in actions[device]:
                fp.write('"{}","{}","{}"\n'.format(printDate(CurTime),device, actions[device][TargetMinute]))
        CurTime = CurTime + datetime.timedelta(minutes=15)
