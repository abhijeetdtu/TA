%load_ext autoreload
%autoreload 2

from TA.Login.Login import Login , Browser
from bs4 import  BeautifulSoup

import pandas as pd
from enum import Enum
import time

class URLS:
    SEARCH_BASE="https://www.linkedin.com/search/results/people/?keywords={}&origin=GLOBAL_SEARCH_HEADER"


def _safeText(text):
    return text.strip("\n")

keywords =["mohit" , "saini"]
def getKeywordsResults(keywords):
    keywordsStr = "&".join(keywords)
    selector = ".search-results__list"
    waitForSelector = ".search-result__wrapper  .subline-level-1"
    indivResult = ".search-result--person"
    linkSelector = "a.search-result__result-link"
    nameSelector = "span.actor-name"
    sublineSelector = "p.subline-level-1"
    locationSelector = "p.subline-level-2"
    url = URLS.SEARCH_BASE.format(keywordsStr)
    resp = Login._waitForUrl(url , waitForSelector , 10)
    soup = BeautifulSoup(resp.page_source)
    results = soup.select_one(selector)
    allResults = results.select(indivResult)
    #r= allResults[0]
    profiles = []
    for r in allResults:

        profileURL = r.select_one(linkSelector)["href"]
        name = r.select_one(nameSelector).text
        subline = r.select_one(sublineSelector).text
        location = r.select_one(locationSelector).text
        subline = _safeText(subline)
        location = _safeText(location)
        obj = {"link" : profileURL , "name" : name , "subline":subline , "location" : location}
        print(obj)
        profiles.append(obj)

    return profiles


def Stalk(peopleNames ,filename="temp.csv", throttle=10):
    allProfiles = []
    for name in peopleNames:
        profiles = getKeywordsResults([name])
        allProfiles.extend(profiles)
        time.sleep(throttle)

    df = pd.DataFrame(allProfiles)
    df.to_csv(filename)

Browser(force=True)

getKeywordsResults(["shruti" , "senoy"])

Stalk(["abhijeet pokhriyal" , "shruti senoy" , "joshua hertel"])
