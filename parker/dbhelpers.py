__author__ = 'ctepasiam2'
from django.db.models import Model
from parker.models import Parking, RatePrice, RateType


def geo_search(self, min_lat, max_lat, min_long, max_long):
    """
    We assume that search boundaries are small enough so there is no need to do complex
    spherical calculations of latitude and longitude.

    Returns: All Parking's model objects within given boundary
    """

    parkings = Parking.object.filter(lat__gte=min_lat, lat__lte=max_lat, long__gte=min_long, long__lte=max_long)

    return parkings.all()
