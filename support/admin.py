from django.contrib import admin
from .models import SupportTicket, TicketReply


class TicketReplyInline(admin.TabularInline):
    model = TicketReply


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'priority', 'assigned_to', 'created')
    list_filter = ('status', 'priority', 'created')
    search_fields = ('subject', 'user__username')
    inlines = [TicketReplyInline]
