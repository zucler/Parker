from django.contrib import admin

from parker.models.common import Parking, RateType, RatePrice

admin.site.register(Parking)
admin.site.register(RateType)
admin.site.register(RatePrice)
