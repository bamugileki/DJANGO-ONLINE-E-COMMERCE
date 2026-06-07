from django.db import models
from django.conf import settings

class LoyaltyPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loyalty_points')
    points = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=200, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='loyalty_points')
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Loyalty points'
    
    def __str__(self):
        return f'{self.user.username} - {self.points} pts'
