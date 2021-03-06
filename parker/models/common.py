from django.db import models
from datetime import time

PARKING_TYPES = (
    ('WILSON', 'Wilson'),
    ('SECURE', 'Secure Parking'),
)

RATE_TYPES = (
    ('Hourly', 'Hourly'),
    ('Flat', 'Flat'),
)


class Parking(models.Model):
    parkingID = models.AutoField(primary_key=True, unique=True)
    #enabled = models.BooleanField(default=False)
    label = models.CharField(max_length=500)
    address = models.TextField(default="")
    lat = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    long = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    parking_type = models.CharField(max_length=150, choices=PARKING_TYPES)
    places_of_interest = models.TextField(default="")     # TODO: Need to be a separate table
    uri = models.TextField()

    def __str__(self):
        return self.label


class RateType(models.Model):
    """
    day_of_week --- Weekday index for date (1 = Sunday, 2 = Monday, ..., 7 = Saturday). Corresponds to ODBC standard
    """
    parkingID = models.ForeignKey(Parking, on_delete=models.CASCADE, db_column='parkingID')
    rateID = models.AutoField(primary_key=True, unique=True)
    day_of_week = models.SmallIntegerField(default=0)
    start_time = models.TimeField(default=time(0, 0, 0))
    end_time = models.TimeField(default=time(0, 0, 0))
    rate_type = models.CharField(max_length=50, choices=RATE_TYPES)
    label = models.CharField(max_length=50, default="")

    def __str__(self):
        obj_label = self.parkingID.label + " - " + self.rate_type + " - " + self.label

        if self.day_of_week:
            obj_label += " - " + str(self.day_of_week)

        return obj_label

    class Meta:
        unique_together = ('parkingID', 'day_of_week', 'rate_type', 'label')


class RatePrice(models.Model):
    rateID = models.ForeignKey(RateType, on_delete=models.CASCADE, db_column='rateID')
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    def __str__(self):
        obj_label = self.rateID.__str__()

        if self.rateID.rate_type == "Hourly":
            obj_label += " [" + str(self.duration) + "]"

        return obj_label

    class Meta:
        unique_together = ('duration', 'rateID')


class EverythingModel(models.Model):
    pp = Parking
    rt = RateType
    rp = RatePrice

    class Meta:
        abstract=True
