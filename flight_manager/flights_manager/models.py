from django.db import models

# Create your models here.
class Carrier(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')
    name = models.CharField(max_length=255, verbose_name='Nombre')

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = 'Aerolínea'
        verbose_name_plural = 'Aerolíneas'

class Place(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'

class Leg(models.Model):
    id = models.CharField(primary_key=True, max_length=20, verbose_name='ID del Tramo')
    departure_airport = models.ForeignKey(Place, related_name='departures', on_delete=models.CASCADE, verbose_name='Aeropuerto de Salida')
    arrival_airport = models.ForeignKey(Place, related_name='arrivals', on_delete=models.CASCADE, verbose_name='Aeropuerto de Llegada')
    departure_time = models.DateTimeField(verbose_name='Hora de Salida')
    arrival_time = models.DateTimeField(verbose_name='Hora de Llegada')
    stops = models.IntegerField(verbose_name='Escalas')
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, verbose_name='Aerolínea')
    duration_mins = models.IntegerField(verbose_name='Duración (minutos)')

    def __str__(self):
        return f"{self.departure_airport} - {self.arrival_airport} ({self.carrier})"

    class Meta:
        verbose_name = 'Tramo de Vuelo'
        verbose_name_plural = 'Tramos de Vuelo'
class Itinerary(models.Model):
    id = models.CharField(primary_key=True, max_length=20, verbose_name='ID del Itinerario')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    agent = models.CharField(max_length=255, verbose_name='Agente')
    agent_rating = models.FloatField(null=True, blank=True, verbose_name='Calificación de la agencia')
    legs = models.ManyToManyField(Leg, related_name='itineraries', verbose_name='Tramos')

    def __str__(self):
        return f"Itinerario {self.id} - {self.agent} (£{self.price})"

    class Meta:
        verbose_name = 'Itinerario'
        verbose_name_plural = 'Itinerarios'