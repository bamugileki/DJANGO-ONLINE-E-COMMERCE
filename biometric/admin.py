from django.contrib import admin
from .models import FaceDescriptor, BiometricSession

@admin.register(FaceDescriptor)
class FaceDescriptorAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'enrolled_at')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__email')

@admin.register(BiometricSession)
class BiometricSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('is_verified',)
    search_fields = ('user__username',)
