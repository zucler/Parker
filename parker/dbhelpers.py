from parker.models import Parking, RatePrice, RateType


def geo_search_all_models(min_lat, max_lat, min_long, max_long):
    """
    Returns: All Parking's model objects within given boundary
    """

    # INFO: All the arguments validation happens in child functions

    parkings = Parking.objects.filter(lat__gte=min_lat, lat__lte=max_lat, long__gte=min_long, long__lte=max_long).all()
    rtype = RateType.objects.filter(parkingID__in=parkings).all()
    rprice = RatePrice.objects.filter(rateID__in=rtype).all()

    # To cache whole querysets
    # FIXME: We need workaround where no extra work done
    bool(parkings)
    bool(rtype)
    bool(rprice)

    everything = {
        'parkings': parkings,
        'ratetype': rtype,
        'rateprice': rprice,
    }

    return everything
