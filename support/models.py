from django.db import models
from django.conf import settings


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.subject} ({self.get_status_display()})'


class TicketReply(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Reply by {self.user.username}'


class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('payment', 'Payment Issues'),
        ('vendor', 'Vendor Support'),
        ('technical', 'Technical Support'),
    ]
    VENDOR_SUBJECTS = [
        ('product_approval', 'Product approval'),
        ('store_management', 'Store management'),
        ('payout', 'Payout issues'),
        ('commission', 'Commission inquiries'),
    ]
    TECHNICAL_SUBJECTS = [
        ('login', 'Login problems'),
        ('bug', 'System bugs'),
        ('api', 'API issues'),
        ('security', 'Security concerns'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attachment = models.FileField(upload_to='contact_attachments/', blank=True)
    status = models.CharField(max_length=20, choices=SupportTicket.STATUS_CHOICES, default='open')
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Contact messages'

    def __str__(self):
        return f'{self.full_name} - {self.subject}'


class ContactReply(models.Model):
    contact = models.ForeignKey(ContactMessage, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Reply by {self.user.username}'
