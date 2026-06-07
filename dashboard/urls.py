from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('vendors/', views.vendor_approvals, name='vendor_approvals'),
    path('vendors/approve/<int:vendor_id>/', views.vendor_approve, name='vendor_approve'),
    path('vendors/reject/<int:vendor_id>/', views.vendor_reject, name='vendor_reject'),
    path('users/', views.manage_users, name='manage_users'),
    path('employees/', views.manage_employees, name='manage_employees'),
    path('admin/<slug:app_label>/<slug:model_name>/', views.model_list, name='model_list'),
    path('admin/<slug:app_label>/<slug:model_name>/add/', views.model_add, name='model_add'),
    path('admin/<slug:app_label>/<slug:model_name>/<int:pk>/change/', views.model_edit, name='model_edit'),
    path('admin/<slug:app_label>/<slug:model_name>/<int:pk>/delete/', views.model_delete, name='model_delete'),
]
