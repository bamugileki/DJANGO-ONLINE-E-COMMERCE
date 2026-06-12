from django.contrib import admin
from .models import SiteSettings, Banner, FAQ, CMSPage


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'currency')
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'site_tagline', 'logo', 'favicon', 'footer_text')}),
        ('Contact', {'fields': ('contact_email', 'contact_phone', 'address')}),
        ('Shop Config', {'fields': ('currency', 'tax_rate', 'free_shipping_threshold', 'is_setup_complete')}),
        ('Authentication', {'fields': ('login_method',), 'description': 'Choose which login methods users can use to access the platform.'}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(SiteSettings, SiteSettingsAdmin)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_filter = ('is_active',)


@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
