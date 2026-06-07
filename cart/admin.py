from django.contrib import admin
from .models import Cart, CartItem, Wishlist


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated')
    list_filter = ('created',)
    inlines = [CartItemInline]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created')
    list_filter = ('created',)
    search_fields = ('user__username', 'product__name')
