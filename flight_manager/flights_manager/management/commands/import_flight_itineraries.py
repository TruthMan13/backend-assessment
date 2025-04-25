from django.core.management.base import BaseCommand
import requests
import json
from flights_manager.models import Carrier, Place, Leg, Itinerary
from django.utils import timezone
from datetime import timezone as datetime_timezone

class Command(BaseCommand):
    help = 'Imports flight data from the provided URL into the database'

    def handle(self, *args, **options):
        url = "https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json"
        flight_data = self.fetch_json_data(url)

        if flight_data:
            self.stdout.write(self.style.SUCCESS('Successfully fetched JSON data.'))
            itineraries = flight_data.get('itineraries', [])
            legs = flight_data.get('legs', [])

            self.stdout.write(f"Number of itineraries found: {len(itineraries)}")
            self.stdout.write(f"Number of flight legs found: {len(legs)}")

            for leg_data in legs:
                carrier, created = Carrier.objects.get_or_create(
                    code=leg_data.get('airline_id'),
                    defaults={'name': leg_data.get('airline_name', 'Unknown Airline')}
                )
                departure_airport, created = Place.objects.get_or_create(code=leg_data.get('departure_airport'))
                arrival_airport, created = Place.objects.get_or_create(code=leg_data.get('arrival_airport'))

                departure_time_str = leg_data.get('departure_time')
                arrival_time_str = leg_data.get('arrival_time')
                departure_time = timezone.datetime.fromisoformat(departure_time_str).replace(tzinfo=datetime_timezone.utc)
                arrival_time = timezone.datetime.fromisoformat(arrival_time_str).replace(tzinfo=datetime_timezone.utc)

                leg = Leg(
                    id=leg_data.get('id'),
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    stops=leg_data.get('stops'),
                    carrier=carrier,
                    duration_mins=leg_data.get('duration_mins')
                )
                leg.save()
                self.stdout.write(self.style.SUCCESS(f'Leg saved: {leg.id}'))

            for itinerary_data in itineraries:
                itinerary = Itinerary(
                    id=itinerary_data.get('id'),
                    price=float(itinerary_data.get('price').replace('£', '')),
                    agent=itinerary_data.get('agent'),
                    agent_rating=itinerary_data.get('agent_rating')
                )
                itinerary.save()
                self.stdout.write(self.style.SUCCESS(f'Itinerary saved: {itinerary.id}'))
                for leg_id in itinerary_data.get('legs', []):
                    try:
                        leg = Leg.objects.get(id=leg_id)
                        itinerary.legs.add(leg)
                    except Leg.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Warning: Leg with ID {leg_id} not found for itinerary {itinerary.id}'))

            self.stdout.write(self.style.SUCCESS('Successfully imported all flight data.'))

    def fetch_json_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching data from URL: {e}'))
            return None
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Error decoding JSON response: {e}'))
            return None