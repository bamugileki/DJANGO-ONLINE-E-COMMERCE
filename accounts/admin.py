from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Address, EmployeeProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'get_role', 'is_staff', 'date_joined')
    list_filter = ('profile__role', 'is_staff', 'is_superuser')

    def get_role(self, obj):
        return obj.profile.get_role_display()
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'city', 'country', 'is_default')
    list_filter = ('address_type', 'is_default', 'country')


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'position', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('user__username', 'employee_id', 'department')
