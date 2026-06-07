from django.db import models
from django.conf import settings

class FaceDescriptor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='face_descriptor')
    embedding = models.TextField(help_text='Encrypted face embedding vector as base64 string')
    is_active = models.BooleanField(default=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Face Descriptor'
        verbose_name_plural = 'Face Descriptors'

    def __str__(self):
        return f'Face descriptor for {self.user.username}'

class BiometricSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='biometric_sessions')
    session_token = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Biometric Session'
        verbose_name_plural = 'Biometric Sessions'

    def __str__(self):
        return f'Biometric session for {self.user.username}'
