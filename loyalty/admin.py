from django.contrib import admin
from .models import LoyaltyPoints


@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'reason', 'created', 'expires_at')
    list_filter = ('created',)
    search_fields = ('user__username', 'reason')
