from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='MimicME Shop')
    site_tagline = models.CharField(max_length=500, blank=True, default='Your Premier E-Commerce Platform')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    footer_text = models.CharField(max_length=500, blank=True, default='Built with Django & Bootstrap')
    contact_email = models.EmailField(blank=True, default='francis@mimicmeshop.com')
    contact_phone = models.CharField(max_length=20, blank=True, default='+255689045666')
    address = models.CharField(max_length=500, blank=True, default='456 Main St, Dodoma')
    currency = models.CharField(max_length=10, default='TSh')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    is_setup_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='banners/')
    link_url = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.question

class CMSPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
