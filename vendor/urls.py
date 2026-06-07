from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_dashboard, name='vendor_dashboard'),
    path('apply/', views.vendor_apply, name='vendor_apply'),
    path('products/', views.vendor_products, name='vendor_products'),
    path('products/add/', views.vendor_product_add, name='vendor_product_add'),
    path('products/edit/<int:product_id>/', views.vendor_product_edit, name='vendor_product_edit'),
    path('products/delete/<int:product_id>/', views.vendor_product_delete, name='vendor_product_delete'),
    path('orders/', views.vendor_orders, name='vendor_orders'),
    path('earnings/', views.vendor_earnings, name='vendor_earnings'),
    path('earnings/withdraw/', views.vendor_withdrawal_request, name='vendor_withdrawal_request'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
]
