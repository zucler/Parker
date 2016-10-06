from django.db.models import Q

from parker.models import Parking, RatePrice, RateType


def geo_search_all_models(s, w, n, e):
    """
    Returns: All Parking's model objects within given boundary
    """

    # INFO: All the arguments validation happens in child functions

    if w > e: # could happen only when 180 meridian crossed
        longLookupQuery = Q(long__gte=e, long__lte=180) | Q(long__lte=w, long__gte=-180)
    else:
        longLookupQuery = Q(long__gte=w, long__lte=e)


    parkings = Parking.objects.filter(lat__gte=s, lat__lte=n).filter(longLookupQuery).all()
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
