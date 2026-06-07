from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariation, ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'vendor', 'price', 'stock', 'available', 'created')
    list_filter = ('available', 'category', 'brand', 'vendor', 'created')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariationInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created')


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value', 'price_adjustment', 'stock', 'sku')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created')
    list_filter = ('is_approved', 'rating', 'created')
    search_fields = ('product__name', 'user__username')
