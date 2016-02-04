from rest_framework import serializers

from parker.models import PARKING_TYPES, RATE_TYPES


class RatePriceSerializer(serializers.Serializer):
    rateID_id = serializers.IntegerField(read_only=True)
    duration = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=6, default=0)


class RateTypeSerializer(serializers.Serializer):
    parkingID_id = serializers.IntegerField(read_only=True)
    rateID = serializers.IntegerField(read_only=True)
    day_of_week = serializers.IntegerField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    rate_type = serializers.ChoiceField(choices=RATE_TYPES, default="Flat")
    label = serializers.CharField(max_length=50, default="")
    rateprice = RatePriceSerializer(many=True, required=False)


class ParkingSerializer(serializers.Serializer):
    parkingID = serializers.IntegerField(read_only=True)
    label = serializers.CharField(max_length=500)
    address = serializers.CharField()
    lat = serializers.DecimalField(max_digits=10, decimal_places=6, default=0)
    long = serializers.DecimalField(max_digits=10, decimal_places=6, default=0)
    parking_type = serializers.ChoiceField(choices=PARKING_TYPES)
    places_of_interest = serializers.CharField()
    uri = serializers.URLField()
    ratetype = RateTypeSerializer(many=True, required=False)

# edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
