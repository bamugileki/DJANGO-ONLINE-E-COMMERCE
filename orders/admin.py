from django.contrib import admin
from .models import Order, OrderItem, Refund, Return


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'paid', 'status', 'created')
    list_filter = ('paid', 'status', 'created')
    search_fields = ('id', 'first_name', 'last_name', 'email')
    inlines = [OrderItemInline]


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'status', 'created')
    list_filter = ('status', 'created')


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'created')
    list_filter = ('status', 'created')
