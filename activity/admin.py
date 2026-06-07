from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'description', 'ip_address', 'created')
    list_filter = ('action', 'created')
    search_fields = ('user__username', 'description', 'model_name')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'created')
