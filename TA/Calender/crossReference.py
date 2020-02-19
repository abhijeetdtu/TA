from bs4 import BeautifulSoup
import requests


def _getURLSoup():
    calenderUrl = "https://datascience.uncc.edu/upcoming-events"
    page = requests.get(calenderUrl)
    page
    page.text

    soup = BeautifulSoup(page.text)
    #clist = soup.find("div" , {"class" : "view-features-events-lists"})
    return soup

class SDSEvent:

    def __init__(self , name , date , time , location):
        self.name = name
        self.date = date
        self.time = time
        self.location = location

    def Print(self):
        print(f"{self.name} - {self.date} - {self.time} - {self.location}")

def _getDateTime(event):
    try:
        date,time = [e.text for e in event.select("span[class*='date-display-range']")]
    except:
        date,time = event.find_all("span" , {"class" : "date-display-single"})
        date = date.text
        time = time.text

    return date,time

def _getLocation(event):
    try:
        location = event.find("i" , {"class" : "fa-map-marker"}).next_sibling
        location = location.strip(" ")
    except:
        location = "**Not Specified**"

    return location

def getEvents():
    orgEvents = []
    soup = _getURLSoup()
    events = soup.select("div.views-row")
    len(events)
    for i,event in enumerate(events):
        #i = 6
        #event = events[i]
        heading = event.find("h3").text
        date,time = _getDateTime(event)
        location = _getLocation(event)
        orgEvents.append(SDSEvent(heading,date ,time,location ))
    return orgEvents


[e.Print() for e in getEvents()]
