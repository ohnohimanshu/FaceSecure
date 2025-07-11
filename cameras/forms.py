from django import forms
from .models import Camera

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['name', 'ip_address', 'port', 'username', 'password', 'is_active', 'face_detection_enabled']