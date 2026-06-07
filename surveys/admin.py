from django.contrib import admin
from .models import TamUtautSurvey, TrustMetric

@admin.register(TamUtautSurvey)
class TamUtautSurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'pu_average', 'peu_average', 'trust_average', 'bi_intend_to_use', 'submitted_at')
    list_filter = ('submitted_at', 'role_at_time')
    search_fields = ('user__username', 'user__email')

@admin.register(TrustMetric)
class TrustMetricAdmin(admin.ModelAdmin):
    list_display = ('user', 'metric_name', 'score', 'recorded_at')
    list_filter = ('metric_name', 'recorded_at')
    search_fields = ('user__username',)
