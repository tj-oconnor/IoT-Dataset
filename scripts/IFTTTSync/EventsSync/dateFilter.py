import re
import sys
import json
import datetime
import csv
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
def filter(file, outputFormat):

    with open(file + ".csv", 'w') as wp:
        with open(file + ".csv.raw",'r') as rp:
            reader = csv.reader(rp)
            for line in reader:
                curDate = parseDate(line[0])
                if (line[2] == "IoTLab-KwikSet-Door Lock"):
                    line[1] = "kwikset-lock-01"
                    if line[3].lower() == "locked":
                        line[2] = "event_lock"
                    else:
                        line[2] = "event_unlock"
                if (line[1] == "schlage lock 01"):
                    line[1] = "schlage-lock-01"
                if (line[1] == "sifely-biometric-lock"):
                    line[1] = "sifely-lock-01"
                line[1] = line[1].lower()
                if curDate > after and curDate < before:
                    wp.write("\"{}\",\"{}\",\"{}\"\n".format(curDate.strftime(outputFormat), line[1], line[2]))

filter("ifttt-events", "%B %d, %Y at %I:%M%p")
filter("android-events", "%B %d, %Y at %I:%M:%S%p")