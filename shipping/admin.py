from django.contrib import admin
from .models import ShippingZone, ShippingRate, Shipment


@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)


@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'price', 'estimated_days', 'is_free', 'is_active')
    list_filter = ('zone', 'is_free', 'is_active')


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'carrier', 'tracking_number', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('order__id', 'tracking_number')
