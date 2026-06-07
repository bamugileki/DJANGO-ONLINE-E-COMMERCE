from django.urls import path
from . import views

urlpatterns = [
    path('enrollment/', views.enrollment, name='biometric_enrollment'),
    path('save-descriptor/', views.save_face_descriptor, name='biometric_save'),
    path('verify/', views.verify_face, name='biometric_verify'),
    path('verify-descriptor/', views.verify_face_descriptor, name='biometric_verify_descriptor'),
]
