from django.contrib import admin
from .models import Vendor, VendorPayout, Withdrawal


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'business_type', 'is_approved', 'is_active', 'commission_rate', 'total_earnings', 'created')
    list_filter = ('is_approved', 'is_active', 'business_type', 'created')
    search_fields = ('business_name', 'user__username', 'business_email', 'registration_number')
    readonly_fields = ('total_earnings', 'available_balance')
    fieldsets = (
        ('User & Status', {'fields': ('user', 'is_approved', 'is_active', 'commission_rate')}),
        ('Business Info', {'fields': ('business_name', 'business_type', 'business_email', 'phone', 'registration_number', 'tax_id', 'description')}),
        ('Address', {'fields': ('address', 'city', 'country')}),
        ('Documents', {'fields': ('logo', 'national_id_image', 'business_license_image', 'tax_certificate')}),
        ('Banking', {'fields': ('bank_name', 'account_name', 'account_number', 'mobile_money_number', 'payment_preference')}),
        ('Financials', {'fields': ('total_earnings', 'available_balance')}),
    )


@admin.register(VendorPayout)
class VendorPayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'amount', 'status', 'payment_method', 'created')
    list_filter = ('status', 'created')
    search_fields = ('vendor__business_name',)


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'amount', 'status', 'payment_method', 'created')
    list_filter = ('status', 'created')
    search_fields = ('vendor__business_name',)
