from django.db import models
from django.conf import settings

class TamUtautSurvey(models.Model):
    AGREEMENT_CHOICES = [
        (1, 'Strongly Disagree'),
        (2, 'Disagree'),
        (3, 'Neutral'),
        (4, 'Agree'),
        (5, 'Strongly Agree'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # Perceived Usefulness (PU)
    pu_speeds_up = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='The system helps me complete transactions faster')
    pu_improves_performance = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='The system improves my shopping performance')
    pu_useful = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='The system is useful for online shopping')
    # Perceived Ease of Use (PEOU)
    peu_easy_to_learn = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='Learning to use the system is easy')
    peu_easy_to_use = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='The system is easy to use')
    peu_clear_interaction = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='My interaction with the system is clear and understandable')
    # Performance Expectancy (PE)
    pe_saves_time = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='The system saves me time when shopping')
    pe_increases_productivity = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='The system increases my shopping productivity')
    # Effort Expectancy (EE)
    ee_effortless = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I find the system effortless to use')
    ee_easy_to_navigate = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='Navigation through the system is easy')
    # Social Influence (SI)
    si_others_recommend = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='People who influence me think I should use the system')
    si_peers_use = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='My peers use similar systems')
    # Facilitating Conditions (FC)
    fc_resources_available = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I have the resources needed to use the system')
    fc_support_available = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='Help and support is available when I need it')
    # Trust
    trust_system = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I trust the system to protect my data')
    trust_payment = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I trust the payment processing')
    trust_vendor = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I trust vendors on this platform')
    # Behavioral Intention (BI)
    bi_intend_to_use = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I intend to continue using the system')
    bi_would_recommend = models.IntegerField(choices=AGREEMENT_CHOICES, verbose_name='I would recommend the system to others')
    # Open feedback
    feedback = models.TextField(blank=True, help_text='Additional comments or feedback')
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    role_at_time = models.CharField(max_length=20, blank=True, help_text='User role when survey was taken')

    class Meta:
        verbose_name = 'TAM/UTAUT Survey'
        verbose_name_plural = 'TAM/UTAUT Surveys'

    def __str__(self):
        return f'Survey by {self.user.username if self.user else "Anonymous"} on {self.submitted_at.date()}'

    def pu_average(self):
        vals = [self.pu_speeds_up, self.pu_improves_performance, self.pu_useful]
        return round(sum(vals) / len(vals), 2)
    pu_average.short_description = 'PU Avg'

    def peu_average(self):
        vals = [self.peu_easy_to_learn, self.peu_easy_to_use, self.peu_clear_interaction]
        return round(sum(vals) / len(vals), 2)
    peu_average.short_description = 'PEOU Avg'

    def trust_average(self):
        vals = [self.trust_system, self.trust_payment, self.trust_vendor]
        return round(sum(vals) / len(vals), 2)
    trust_average.short_description = 'Trust Avg'


class TrustMetric(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    metric_name = models.CharField(max_length=100, help_text='e.g. login_trust, payment_trust, vendor_trust')
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text='Trust score 0.00 - 5.00')
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Trust Metric'
        verbose_name_plural = 'Trust Metrics'
        ordering = ['-recorded_at']

    def __str__(self):
        return f'{self.metric_name}: {self.score}'
