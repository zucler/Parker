__author__ = 'mpak'

from contextlib import closing

from django.test import TestCase
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from parker.classes.parsers.core.parser import WillsonsRatesParser
from parker.classes.rates import WillsonsRates


class WilssonsRateParserMethodTest(TestCase):
    def test_get_prices_information_with_valid_html(self):
        """
        get_prices_information() should return object of type WillsonsParkingRates
        """
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
            self.assertIsInstance(rates, WillsonsRates)
            self.assertIsInstance(rates.rates, dict)

    def test_get_prices_information_with_invalid_html(self):
        """
        get_prices_information() should return object of type WillsonsParkingRates
        """
        parser = WillsonsRatesParser()
        rates = parser.get_prices_information("This string does not have any pricing")
        self.assertIsInstance(rates, WillsonsRates)
        #self.assertEquals(rates.rates, {})
