from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserInteractionsSingleton:
    _inst_ = None
    def __new__(self):
        if BrowserInteractionsSingleton._inst_ == None:
            BrowserInteractionsSingleton._inst_ = BrowserInteractions()
        return BrowserInteractionsSingleton._inst_

class BrowserInteractions:

    def Click(self,browser,cssSelector):
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector))
        )
        browser.find_element_by_css_selector(cssSelector).click()
