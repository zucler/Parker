import pprint

from bs4 import BeautifulSoup

from parker.models.common import Parking

class AllParkingsList():
    """
        Contains all routines needed to parse and update Wilson parkings list
    """

    def get_list(self, html: str):
        """Returns list of all links parsed from parkings list"""
        soup = BeautifulSoup(html, 'html.parser')
        list = soup.select('section.col-sm-12 ul li a')
        links = [tag['href'] for tag in list]
        return links
