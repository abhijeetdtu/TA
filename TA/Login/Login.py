from TA.Conf import Config
import requests, zipfile , io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import browser_cookie3

import time

class Browser:
    _inst_ = None

    def __new__(self , force=False , args=None):
        if force or Browser._inst_ == None:
            browser = webdriver.Firefox( firefox_profile= Browser.GetProfile(args))
            Browser._inst_ = browser
            return Browser._inst_
        else:
            return Browser._inst_

    @staticmethod
    def GetProfile(args):
        args = args if args != None else {}

        folder = args.get("downloadFolder" , Config.DATA_DUMP_FOLDER)
        print(folder)
        profile = FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", folder)
        profile = Browser._getDefaultPreferences(profile)
        return profile

    def _getDefaultPreferences(profile):
        mime_types = [
            'text/plain',
            'application/vnd.ms-excel',
            'text/csv',
            'application/csv',
            'text/comma-separated-values',
            'application/download',
            'application/octet-stream',
            'binary/octet-stream',
            'application/binary',
            'application/x-unknown',
            "application/zip"
            'application/xlsx',
        ]
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(mime_types))
        return profile

class Login:

    @staticmethod
    def StaticAuthGet( url):
        cj = browser_cookie3.firefox()
        #print(url,cj)
        r = requests.get(url, cookies=cj)
        return r

    @staticmethod
    def DownloadZIP(url , destination):
        cj = browser_cookie3.firefox()
        r = requests.get(url, cookies=cj)
        try:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(destination)
        except Exception as e:
            print(e)

    @staticmethod
    def AuthGet(url):
        cj = browser_cookie3.firefox()
        browser = Browser()
        r = browser.get(url)
        [browser.add_cookie({"name" : c.name , "value":c.value , "domain" : c.domain}) for c in cj if c.domain in ["webauth.uncc.edu"]]
        #[browser.add_cookie({"name" : c.name , "value":c.value , "domain" : c.domain}) for c in cj if url.find( c.domain) > -1 or c.domain == "webauth.uncc.edu"]
        browser.get(url)
        return browser

    @staticmethod
    def GetUrl(url , waitForCssSelector):
        browser = Login._waitForUrl(url , waitForCssSelector)
        return browser.page_source

    @staticmethod
    def _waitForUrl(url , waitForCssSelector , forceSleep=None):
        browser = Login.AuthGet(url)
        element = WebDriverWait(browser, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, waitForCssSelector))
        )
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if forceSleep:
            time.sleep(forceSleep)
        return browser

    @staticmethod
    def GetBrowser(url , waitForCssSelector):
        return Login._waitForUrl(url , waitForCssSelector)
