from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TamUtautSurvey, TrustMetric


@login_required
def survey_view(request):
    already_submitted = TamUtautSurvey.objects.filter(user=request.user).exists()
    if already_submitted:
        messages.info(request, 'You have already submitted a survey. Thank you!')
        return redirect('product_list')

    if request.method == 'POST':
        try:
            survey = TamUtautSurvey(
                user=request.user,
                pu_speeds_up=int(request.POST.get('pu_speeds_up', 3)),
                pu_improves_performance=int(request.POST.get('pu_improves_performance', 3)),
                pu_useful=int(request.POST.get('pu_useful', 3)),
                peu_easy_to_learn=int(request.POST.get('peu_easy_to_learn', 3)),
                peu_easy_to_use=int(request.POST.get('peu_easy_to_use', 3)),
                peu_clear_interaction=int(request.POST.get('peu_clear_interaction', 3)),
                pe_saves_time=int(request.POST.get('pe_saves_time', 3)),
                pe_increases_productivity=int(request.POST.get('pe_increases_productivity', 3)),
                ee_effortless=int(request.POST.get('ee_effortless', 3)),
                ee_easy_to_navigate=int(request.POST.get('ee_easy_to_navigate', 3)),
                si_others_recommend=int(request.POST.get('si_others_recommend', 3)),
                si_peers_use=int(request.POST.get('si_peers_use', 3)),
                fc_resources_available=int(request.POST.get('fc_resources_available', 3)),
                fc_support_available=int(request.POST.get('fc_support_available', 3)),
                trust_system=int(request.POST.get('trust_system', 3)),
                trust_payment=int(request.POST.get('trust_payment', 3)),
                trust_vendor=int(request.POST.get('trust_vendor', 3)),
                bi_intend_to_use=int(request.POST.get('bi_intend_to_use', 3)),
                bi_would_recommend=int(request.POST.get('bi_would_recommend', 3)),
                feedback=request.POST.get('feedback', ''),
                role_at_time=request.POST.get('role_at_time', request.user.profile.role if hasattr(request.user, 'profile') else ''),
            )
            survey.save()
            TrustMetric.objects.create(
                user=request.user,
                metric_name='overall_trust',
                score=survey.trust_average(),
            )
            messages.success(request, 'Survey submitted successfully. Thank you for your feedback!')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error submitting survey: {e}')

    return render(request, 'surveys/survey.html')
