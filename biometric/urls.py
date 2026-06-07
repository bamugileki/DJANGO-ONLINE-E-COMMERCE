from django.urls import path
from . import views

urlpatterns = [
    path('enrollment/', views.enrollment, name='biometric_enrollment'),
    path('save-descriptor/', views.save_face_descriptor, name='biometric_save'),
    path('verify/', views.verify_face, name='biometric_verify'),
    path('verify-descriptor/', views.verify_face_descriptor, name='biometric_verify_descriptor'),
    path('facial-login/', views.facial_login, name='biometric_facial_login'),
    path('facial-login-verify/', views.facial_login_verify, name='biometric_facial_login_verify'),
]
