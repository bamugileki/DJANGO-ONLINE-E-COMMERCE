from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_history, name='order_history'),
    path('receipt/<int:order_id>/', views.receipt_detail, name='receipt_detail'),
]
