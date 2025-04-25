# flights_manager/views.py
from rest_framework import viewsets
from rest_framework import filters
from .models import Leg
from .serializers import LegSerializer

class FlightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leg.objects.all()
    serializer_class = LegSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['departure_airport__code', 'arrival_airport__code', 'carrier__name', 'carrier__code']

    # Ejemplo de filtro personalizado por aeropuerto de salida (opcional)
    def get_queryset(self):
        queryset = super().get_queryset()
        departure_airport = self.request.query_params.get('departure_airport', None)
        if departure_airport:
            queryset = queryset.filter(departure_airport__code__iexact=departure_airport)
        return queryset