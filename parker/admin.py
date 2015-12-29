from django.contrib import admin

from .models import Parking
from .models import RateType
from .models import RatePrice

admin.site.register(Parking)
admin.site.register(RateType)
admin.site.register(RatePrice)
