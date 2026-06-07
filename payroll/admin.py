from django.contrib import admin
from .models import Payroll, Attendance, SalarySlip


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'bonus', 'deductions', 'net_pay', 'month', 'year', 'is_paid')
    list_filter = ('is_paid', 'month', 'year')
    search_fields = ('employee__username',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'is_present')
    list_filter = ('is_present', 'date')
    search_fields = ('employee__username',)


@admin.register(SalarySlip)
class SalarySlipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'gross_salary', 'deductions', 'net_salary', 'is_generated')
    list_filter = ('is_generated',)
    search_fields = ('employee__username',)
