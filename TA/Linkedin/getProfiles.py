%load_ext autoreload
%autoreload 2

from TA.Linkedin.readList import getNamesFromDefaultTXT
from TA.Login.Login import Login , Browser
from bs4 import  BeautifulSoup

import pandas as pd
from enum import Enum
import time
import logging

class URLS:
    LINKDIN_BASE = "https://www.linkedin.com{}"
    SEARCH_BASE="https://www.linkedin.com/search/results/people/?keywords={}&origin=GLOBAL_SEARCH_HEADER"

class IndividualInfo:
    def __init__(self,name, position,company , dates):
        self.name = name
        self.position = position
        self.company = company
        self.dates = dates

    def __str__(self):
        return f"Name : {self.name} , Position : {self.position} , Company : {self.company} , Dates : {self.dates}"

def _safeText(text):
    return text.strip("\n")

keywords =["mohit" , "saini"]
def getKeywordsResults(keywords ,numProfiles):
    keywordsStr = "&".join(keywords)
    selector = ".search-results__list"
    waitForSelector = ".search-result__wrapper  .subline-level-1"
    indivResult = ".search-result--person"
    linkSelector = "a.search-result__result-link"
    nameSelector = "span.actor-name"
    sublineSelector = "p.subline-level-1"
    locationSelector = "p.subline-level-2"
    url = URLS.SEARCH_BASE.format(keywordsStr)
    logging.info(f"Loading the URL....{url}")
    resp = Login._waitForUrl(url , waitForSelector , 10)

    logging.info("Soup....")
    soup = BeautifulSoup(resp.page_source)
    results = soup.select_one(selector)
    allResults = results.select(indivResult)
    #r= allResults[0]
    profiles = []
    if allResults == None:
        return profiles
    for i,r in enumerate(allResults[:numProfiles]):
        logging.info(f"--{i} profile processing")
        profileURL = r.select_one(linkSelector)["href"]
        name = r.select_one(nameSelector).text
        subline = r.select_one(sublineSelector).text
        location = r.select_one(locationSelector).text
        subline = _safeText(subline)
        location = _safeText(location)
        logging.info("Getting Employment Information....")
        employmentInfo = GetIndivInfo(profileURL)
        obj = {"link" : profileURL , "name" : name , "subline":subline , "location" : location , "employment":employmentInfo}
        print(obj)
        profiles.append(obj)

    return profiles

arr = ['Software Engineer', 'Company Name', 'UnitedHealth Group', 'Full-time', 'Dates Employed', 'Jul 2015 – Jul 2019', 'Employment Duration', '4 yrs 1 mo']
key = "Company Name"
def _findValueFromArray(arr , key):
    try :
        i = arr.index(key)
        return arr[i+1]
    except:
        return "Not Found"

def _extractFromSelectors(elem , selectors):
    possible = [ elem.select_one(s) for s in selectors ]
    return [p.text for p in possible if p is not None]


def _parseInfoObjs(soup , selectorArr):
    infos = []
    for selectora , b , c in selectorArr:
        results = soup.select_one(selectora)

        if results is None:
            return infos
        sections = results.select(b)
        #[ t for t in results.select_one("[data-control-name='background_details_company']").text.split("\n") if t not in ["" , " "]]

        _fa = _findValueFromArray
        for result in sections:
            l = [ t for t in result.select_one(c).text.split("\n") if t not in ["" , " "]]
            infos.append(l)
    return infos

indivLink = "/in/shruti-shenoy-89b05194/"
indivLink = "/in/abhijeet-pokhriyal-18a7649a/"
def GetIndivInfo(indivLink):
    infos= []
    selector = "#experience-section"
    expDetailsSelector = "[data-control-name='background_details_company']"
    educationSelector = "section[data-section='educationsDetails']"
    expDetailsSelector = "a[href*='/company']"
    educationDetailsSelector = "a[href*='/school']"
    summarySection = ".pv-entity__summary-info--background-section"


    url = URLS.LINKDIN_BASE.format(indivLink)

    resp = Login._waitForUrl(url , selector , 10)
    soup = BeautifulSoup(resp.page_source)

    for selector in [educationDetailsSelector ,expDetailsSelector ]:
        lis = soup.select(selector)
        for li in lis:
            parentLi = li.find_parent("li")
            if parentLi is not None:
                l = [ t for t in parentLi.text.split("\n") if t.strip(" \t") not in ["" , " "]]
                infos.append("\n".join(l))
                #print(parentLi.text.split("\n"))

    return infos

#infos = GetIndivInfo(indivLink)

#[print(i) for i in infos ]

def Stalk(peopleNames ,filename="temp.csv", numProfiles=10,throttle=10):

    for name in peopleNames:
        logging.info(f"Looking Up {name}")
        profiles = getKeywordsResults([name] , numProfiles)
        ALL_PROFILES.extend(profiles)
        time.sleep(throttle)

    df = pd.DataFrame(ALL_PROFILES)
    df.to_csv(filename)
    return ALL_PROFILES

logging.basicConfig(level=logging.INFO)
Browser(force=True)

#getKeywordsResults(["shruti" , "senoy"])

#datStalk(["shruti senoy" , "joshua hertel"],numProfiles=2)
ALL_PROFILES = []
peopleList = getNamesFromDefaultTXT()
len(ALL_PROFILES)

data  = Stalk(peopleList,numProfiles=3)

data

allData = []

allData.extend(data)

import json
json.dump(data,open("_test.output2.json" , "w"))


df = pd.DataFrame(ALL_PROFILES)
df.to_csv("_test.output4.csv")
