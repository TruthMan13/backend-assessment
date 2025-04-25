from django.test import TestCase
from .models import Carrier, Place, Leg, Itinerary
from django.utils import timezone as django_timezone  # Para el timezone de Django
from datetime import timezone  # El timezone UTC de Python

class FlightModelsTest(TestCase):

    def test_create_carrier(self):
        carrier = Carrier.objects.create(code='AA', name='American Airlines')
        self.assertEqual(carrier.code, 'AA')
        self.assertEqual(str(carrier), 'American Airlines (AA)')

    def test_create_place(self):
        place = Place.objects.create(code='JFK')
        self.assertEqual(place.code, 'JFK')
        self.assertEqual(str(place), 'JFK')

    def test_create_leg(self):
        carrier = Carrier.objects.create(code='UA', name='United Airlines')
        departure = Place.objects.create(code='SFO')
        arrival = Place.objects.create(code='LAX')
        departure_time = django_timezone.datetime(2025, 4, 25, 10, 0, tzinfo=timezone.utc)
        arrival_time = django_timezone.datetime(2025, 4, 25, 11, 30, tzinfo=timezone.utc)
        leg = Leg.objects.create(
            id='leg_test',
            departure_airport=departure,
            arrival_airport=arrival,
            departure_time=departure_time,
            arrival_time=arrival_time,
            stops=0,
            carrier=carrier,
            duration_mins=90
        )
        self.assertEqual(leg.departure_airport, departure)
        self.assertEqual(leg.carrier.name, 'United Airlines')

    def test_create_itinerary_and_add_leg(self):
        carrier = Carrier.objects.create(code='B6', name='JetBlue')
        origin = Place.objects.create(code='BOS')
        destination = Place.objects.create(code='FLL')
        departure_time = django_timezone.datetime(2025, 4, 25, 14, 0, tzinfo=timezone.utc)
        arrival_time = django_timezone.datetime(2025, 4, 25, 17, 0, tzinfo=timezone.utc)
        leg = Leg.objects.create(
            id='leg_it_test',
            departure_airport=origin,
            arrival_airport=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            stops=0,
            carrier=carrier,
            duration_mins=180
        )
        itinerary = Itinerary.objects.create(id='it_test', price=150.00, agent='JetBlue.com')
        itinerary.legs.add(leg)
        self.assertEqual(itinerary.legs.count(), 1)
        self.assertEqual(itinerary.legs.first().departure_airport.code, 'BOS')