from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cms import views as cms_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('vendor/', include('vendor.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('biometric/', include('biometric.urls')),
    path('survey/', include('surveys.urls')),
    path('contact/', cms_views.contact, name='contact'),
    path('privacy/', cms_views.policy_view, {'slug': 'privacy'}, name='policy_privacy'),
    path('terms/', cms_views.policy_view, {'slug': 'terms'}, name='policy_terms'),
    path('payment-policy/', cms_views.policy_view, {'slug': 'payment'}, name='policy_payment'),
    path('refund-policy/', cms_views.policy_view, {'slug': 'refund'}, name='policy_refund'),
    path('shipping-policy/', cms_views.policy_view, {'slug': 'shipping'}, name='policy_shipping'),
    path('vendor-policy/', cms_views.policy_view, {'slug': 'vendor'}, name='policy_vendor'),
    path('security-policy/', cms_views.policy_view, {'slug': 'security'}, name='policy_security'),
    path('admin-rights/', cms_views.policy_view, {'slug': 'admin-rights'}, name='policy_admin_rights'),
    path('', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
