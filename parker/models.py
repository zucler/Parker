from django.db import models

RATE_TYPES = (
    ('WILSON', 'Wilson'),
    ('SECURE', 'Secure Parking'),
)


class Parking(models.Model):
    parkingID = models.AutoField(primary_key=True, unique=True)
    label = models.CharField(max_length=500)
    address = models.TextField()
    lat = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=10, decimal_places=6, default=0)
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
    label = models.CharField(max_length=50, default="")

    def __str__(self):
        obj_label = self.parkingID.label + " - " + self.type + " - " + self.label

        if self.day_of_week:
            obj_label += " - " + self.day_of_week

        return obj_label


class RatePrice(models.Model):
    rateID = models.ForeignKey(RateType, on_delete=models.CASCADE, db_column='rateID')
    duration = models.CharField(max_length=50)
    price = models.CharField(max_length=50)

    def __str__(self):
        obj_label = self.rateID.__str__()

        if self.rateID.type == "Hourly":
            obj_label += " [" + self.duration + "]"

        return obj_label
