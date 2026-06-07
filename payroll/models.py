from django.db import models
from django.conf import settings

class Payroll(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payrolls')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ('employee', 'month', 'year')
    
    def __str__(self):
        return f'{self.employee.username} - {self.month}/{self.year}'

class Attendance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    is_present = models.BooleanField(default=False)
    notes = models.CharField(max_length=250, blank=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ('employee', 'date')
    
    def __str__(self):
        return f'{self.employee.username} - {self.date}'

class SalarySlip(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='salary_slips')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salary_slips')
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_generated = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Slip - {self.employee.username}'
