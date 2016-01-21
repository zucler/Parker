from rest_framework import serializers


class ParkingSerializer(serializers.Serializer):
    parkingid = serializers.IntegerField(read_only=True)
    label = serializers.CharField(max_length=500)
    address = serializers.CharField()
    lat = serializers.DecimalField(max_digits=10, decimal_places=6, default=0)
    long = serializers.DecimalField(max_digits=10, decimal_places=6, default=0)
    parking_type = serializers.CharField(max_length=150)
    places_of_interest = serializers.CharField()
    uri = serializers.URLField()




