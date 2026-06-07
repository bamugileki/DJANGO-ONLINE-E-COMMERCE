from django.db import models
from orders.models import Order

class ShippingZone(models.Model):
    name = models.CharField(max_length=100)
    countries = models.TextField(help_text='Comma-separated list of countries')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ShippingRate(models.Model):
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name='rates')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.CharField(max_length=50, blank=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name} - TSh{self.price}'

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    shipping_rate = models.ForeignKey(ShippingRate, on_delete=models.SET_NULL, null=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    address_snapshot = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Shipment {self.id} - Order {self.order.id}'
