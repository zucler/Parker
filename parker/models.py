from django.db import models

RATE_TYPES = (
    ('WILSON', 'Wilson'),
    ('SECURE', 'Secure Parking'),
)


class Parking(models.Model):
    parkingID = models.AutoField(primary_key=True, unique=True)
    label = models.CharField(max_length=500)
    address = models.TextField()
    geo_location = models.CharField(max_length=200)
    type = models.CharField(max_length=150, choices=RATE_TYPES)
    places_of_interest = models.TextField()
    uri = models.TextField()

    def __str__(self):
        return self.label


class RateType(models.Model):
    parkingID = models.ForeignKey(Parking, on_delete=models.CASCADE, db_column='parkingID')
    rateID = models.AutoField(primary_key=True, unique=True)
    day_of_week = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=50, choices=RATE_TYPES)


class RatePrices(models.Model):
    rateID = models.ForeignKey(RateType, on_delete=models.CASCADE, db_column='rateID')
    duration = models.IntegerField(default=0)
    price = models.CharField(max_length=50)
