__author__ = 'ctepasiam2'
from django.db.models import Model
from parker.models import Parking, RatePrice, RateType


def geo_search(self, min_lat, max_lat, min_long, max_long):
    """
    We assume that search boundaries are small enough so there is no need to do complex
    spherical calculations of latitude and longitude.

    Returns: All Parking's model objects within given boundary
    """

    # TODO: lng__gte -> long_gte
    parkings = Parking.object.filter(lat__gte=min_lat, lat__lte=max_lat, lng__gte=min_long, lng__lte=max_long)

    return parkings.all()
