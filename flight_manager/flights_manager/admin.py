from django.contrib import admin
from .models import Carrier, Place, Leg, Itinerary
from django.shortcuts import render # Asegúrate de importar render si no lo has hecho

@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)
   


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('code',)
    search_fields = ('code',)
    ordering = ('code',)
     

  

@admin.register(Leg)
class LegAdmin(admin.ModelAdmin):
    list_display = ('id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'carrier')
    list_filter = ('departure_airport', 'arrival_airport', 'carrier')
    search_fields = ('id', 'departure_airport__code', 'arrival_airport__code', 'carrier__name', 'carrier__code')
    ordering = ('departure_time',)
    date_hierarchy = 'departure_time'
     



@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('display_itinerary_id', 'price', 'agent', 'agent_rating', 'display_legs')
    search_fields = ('id', 'agent')
    ordering = ('price',)
    filter_horizontal = ('legs',) # Para la relación ManyToMany
   
    def display_itinerary_id(self, obj):
        return f"Itinerario {obj.id.split('_')[-1]}"
    display_itinerary_id.short_description = 'ID'

    def display_legs(self, obj):
        leg_ids = [f"Leg {leg.id.split('_')[-1]}" for leg in obj.legs.all()]
        return ", ".join(leg_ids)
    display_legs.short_description = 'Legs'
