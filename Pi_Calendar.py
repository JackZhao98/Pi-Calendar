import calendar
from datetime import datetime
import requests
import os
from icalendar import Calendar

class PiCalendarDelegate:
    def __init__(self, root_path = "./CalendarDelegate"):
        self.url = ""
        self.ics_path = ""
        self.root_path = root_path

    def load_url(self, url = None):
        if not url:
            print("Input iCalendar subscription url.")
            exit(1)
        if url.startswith("webcal"):
            url = url.replace("webcal", "https")
        self.url = url

    def subscribe(self):
        return requests.get(self.url)
    
    def download(self):
        resp = requests.get(self.url)
        self.ics_path = os.path.join(self.root_path, 'calendar.ics')
        with open(self.ics_path, 'w') as f:
            f.write(resp.text)

    def read_components(self):
        with open(self.ics_path, 'r') as ics:
            ical = Calendar.from_ical(ics.read())
        events = [e for e in ical.walk('vevent')]
        return events

    def fetch_events(self, url):
        self.load_url(url)
        resp = self.subscribe()
        ical = Calendar.from_ical(resp.text)
        events = [e for e in ical.walk('vevent')]
        return events

    def sanitize(self, events, number = -1):
        today = datetime.timestamp(datetime.now())
        ret = []
        counter = 0
        events = sorted(events, key = lambda i: i['dtstart'].dt)
        for e in events:
            if counter >= number and number >= 0:
                break
            date = datetime.timestamp(e['dtstart'].dt)
            if date < today:
                continue
            else:
                ret.append({'summary':str(e['summary']), 'datestart':e['dtstart'].dt, 'dateend':e['dtend'].dt})
            counter += 1
        return ret


