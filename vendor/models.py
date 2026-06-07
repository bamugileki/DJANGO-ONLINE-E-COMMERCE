from django.db import models
from django.conf import settings


class Vendor(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('partnership', 'Partnership'),
        ('nonprofit', 'Non-Profit'),
    ]
    PAYMENT_PREFERENCE_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_profile',
    )
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default='individual')
    business_email = models.EmailField()
    phone = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True, verbose_name='Tax Identification Number')
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Tanzania')
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='vendors/', blank=True, null=True)
    national_id_image = models.ImageField(upload_to='vendor_docs/', blank=True, null=True)
    business_license_image = models.ImageField(upload_to='vendor_docs/', blank=True, null=True)
    tax_certificate = models.ImageField(upload_to='vendor_docs/', blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    mobile_money_number = models.CharField(max_length=20, blank=True)
    payment_preference = models.CharField(max_length=20, choices=PAYMENT_PREFERENCE_CHOICES, default='mobile_money')
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.business_name


class VendorPayout(models.Model):
    PAYOUT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='payouts',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PAYOUT_STATUS_CHOICES,
        default='pending',
    )
    payment_method = models.CharField(max_length=50)
    payment_details = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payout {self.id} - {self.vendor.business_name}'


class Withdrawal(models.Model):
    WITHDRAWAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='withdrawals',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=WITHDRAWAL_STATUS_CHOICES,
        default='pending',
    )
    payment_method = models.CharField(max_length=50)
    payment_details = models.CharField(max_length=250)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Withdrawal {self.id} - {self.vendor.business_name} - TSh{self.amount}'
