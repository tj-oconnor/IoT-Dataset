import re
import sys
import json
import datetime
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

# when to start counting
after = parseDate("March 08, 2021 at 09:30AM")
before = parseDate("March 15, 2021 at 05:16PM")
#print(after, before)
# expression ->
#   package ->
#     captures -> 
#       field -> regex w/ capture groups
#     mappings -> (events only)
#       capture -> converted
expressions = {
    "com.tplink.kasa_android": {
        "captures": {
            "title": '(?P<device>.*) detected (?P<event>.*)'
        },
        "mappings": {
            "motion": "event_motion",
            "sound": "event_sound"
        }
    },
    "com.merkuryinnovations.geeni": {
        "captures": {
            "text": ['(?P<device>.*) has detected (?P<event>.*).',
                     '(?P<device>.*) someone is (?P<event>.*)!']
        },
        "mappings": {
            "movement": "event_motion",
            "movemen": "event_motion",
            "knocking": "event_ring",
            "sound": "event_sound"
        }
    },
    "com.nest.android": {
        "captures": {
            "title": '(?P<event>.*) \? Office \((?P<device>.*)\)'
        },
        "mappings": {
            "Motion": "event_motion",
            "Sound": "event_sound",
            "Doorbell": "event_ring",
            "Person": "event_person"
        }
    },
    "com.ringapp": {
        "captures": {
            "title": ['There is (?P<event>.*) at your (?P<device>.*)',
                      '\?\? (?P<event>.*) is at your (?P<device>.*)'],
            "text": ['Melbourne (?P<device>.*?)( in IoT Lab)? detected (?P<event>.*) at .*',
                     'Melbourne (?P<device>.*?)( in IoT Lab)? (?P<event>(opened)|(closed)) at .*',
                     'Melbourne (?P<device>.*?)( IoT Lab)? reported (?P<event>.*?) at .*']

        },
        "mappings": {
            "motion": "event_motion",
            "Someone": "event_ring",
            "opened": "event_open",
            "closed": "event_close",
            "low battery": "event_batt"
        }
    },
    "com.simplisafe.mobile": {
        "captures": {
            "text": ['"(?P<device>.*)" Camera Detected (?P<event>.*) on .*',
                     '(?P<event>.*) is at your "(?P<device>.*)" on .*']
        },
        "mappings": {
            "Motion": "event_motion",
            "Someone": "event_ring"
        }
    },
    "com.nightowl.connect": {
        "captures": {
            "text": ["There is (?P<event>.*) at your (?P<device>.*)",
                     'Someone just (?P<event>.*) your (?P<device>.*)']
        },
        "mappings": {
            "motion": "event_motion",
            "rang": "event_ring"
        }
    },
    "com.allegion.leopard": {
        "captures": {
            "text": ["(?P<device>.*?)( is)? (?P<event>(locked)|(unlocked)|(battery low))",
                     "Access code Admin (?P<event>unlocked) (?P<device>.*)"
                     ]
        },
        "mappings": {
            "locked": "event_lock",
            "unlocked": "event_unlock",
            "battery low": "event_batt"
        }
    },
    "com.sifely.smartlock": {
        "captures": {
            "text": "\"(test|123456)\" (?P<event>unlocked) \(\"(?P<device>.*)\"\)\."
        },
        "mappings": {
            "unlocked": "event_unlock"
        }
    }
}


def attemptExtract(obj):
    if not obj["package"] in expressions:
        print("Unknown package", obj["package"], file=sys.stderr)
        return None
    capturedEvent = ""
    capturedDevice = ""

    for element,expression in expressions[obj["package"]]["captures"].items():
        if (capturedEvent and capturedDevice):
            break
        if not element in obj.keys():
            continue
        if isinstance (expression, list):
            for singleExpression in expression:
                match = re.match(singleExpression, obj[element])
                if (match is None):
                    #print("No match in",element, "for", expression,"; data: ", obj, file=sys.stderr)
                    continue
                try:
                    capturedDevice = match.group("device")
                except IndexError:
                    pass

                try:
                    if (not match.group("event") in expressions[obj["package"]]["mappings"].keys()):
                        print("Event", match.group("event"), "found, but no mapping exists.", file=sys.stderr)
                    else:
                        capturedEvent = expressions[obj["package"]]["mappings"][match.group("event")]
                except IndexError:
                    pass
        else:
            match = re.match(expression, obj[element])
            if (match is None):
                #print("No match in",element, "for", expression,"; data: ", obj, file=sys.stderr)
                continue
            try:
                capturedDevice = match.group("device")
            except IndexError:
                pass

            try:
                if (not match.group("event") in expressions[obj["package"]]["mappings"].keys()):
                    print("Event", match.group("event"), "found, but no mapping exists.", file=sys.stderr)
                else:
                    capturedEvent = expressions[obj["package"]]["mappings"][match.group("event")]
            except IndexError:
                pass
    if (capturedEvent and capturedDevice):
        curDate = parseDate(obj["date"])
        if curDate > after and curDate < before:
            print('"%s","%s","%s"' % (obj["date"], capturedDevice.lower(), capturedEvent))
    else:
        print("No match for line", obj, file=sys.stderr)

with open("android-notifications/notifications.json", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        try:
            obj = json.loads(line.strip())
            attemptExtract(obj)
        except json.decoder.JSONDecodeError as e:
            print("JSON Decode Error: ", e)
            print(e)

