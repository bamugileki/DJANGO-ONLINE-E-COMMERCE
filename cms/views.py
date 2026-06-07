from django.shortcuts import render
from django.http import Http404


def contact(request):
    return render(request, 'cms/contact.html')


POLICY_TEMPLATES = {
    'privacy': 'cms/privacy.html',
    'terms': 'cms/terms.html',
    'payment': 'cms/payment.html',
    'refund': 'cms/refund.html',
    'shipping': 'cms/shipping.html',
    'vendor': 'cms/vendor_policy.html',
    'security': 'cms/security.html',
    'admin-rights': 'cms/admin_rights.html',
}


def policy_view(request, slug):
    template = POLICY_TEMPLATES.get(slug)
    if not template:
        raise Http404
    return render(request, template)
