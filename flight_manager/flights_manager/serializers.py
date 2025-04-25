# flights_manager/serializers.py
from rest_framework import serializers
from .models import Leg, Carrier, Place

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ['code', 'name']

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['code']

class LegSerializer(serializers.ModelSerializer):
    departure_airport = PlaceSerializer(read_only=True)
    arrival_airport = PlaceSerializer(read_only=True)
    carrier = CarrierSerializer(read_only=True)

    class Meta:
        model = Leg
        fields = ['id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'stops', 'carrier', 'duration_mins']