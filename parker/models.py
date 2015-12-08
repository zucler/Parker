from django.db import models


class Parking(models.Model):
    parkingID = models.AutoField(primary_key=True, unique=True)
    address = models.TextField()
    geo_location = models.CharField(max_length=200)
    type = models.CharField(max_length=150)
    label = models.CharField(max_length=500)
    places_of_interest = models.TextField()


class RateType(models.Model):
    parkingID = models.ForeignKey(Parking, on_delete=models.CASCADE)
    rateID = models.AutoField(primary_key=True, unique=True)
    day_of_week = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=50)


class RatePrices(models.Model):
    rateID = models.ForeignKey(RateType, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    price = models.CharField(max_length=50)
