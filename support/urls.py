from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.contact_list, name='support_contact_list'),
    path('messages/<int:pk>/', views.contact_detail, name='support_contact_detail'),
]
