__author__ = 'Maxim Pak'

from contextlib import closing

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from parker.parser import WillsonsRatesParser


url = "http://wilsonparking.com.au/park/2036_Queen-Victoria-Building-Car-Park_111-York-Street-Sydney"

# use firefox to get page with javascript generated content
with closing(Firefox()) as browser:
    browser.get(url)
    # wait for the page to load
    WebDriverWait(browser, timeout=10).until(
        lambda x: x.find_element_by_class_name('rates'))
    # store it to string variable
    page_source = browser.page_source
    parser = WillsonsRatesParser()
    rates = parser.get_prices_information(page_source)
    print(rates.rates)
