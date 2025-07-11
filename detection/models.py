from django.db import models
from django.conf import settings
from cameras.models import Camera
from faces.models import Face
from django.core.management.base import BaseCommand
from cameras.models import Camera
from detection.models import Recording
import threading
import cv2
import datetime

class Detection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='detections')
    detected_face = models.ForeignKey(Face, on_delete=models.SET_NULL, null=True, related_name='detections')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confidence_score = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='detections/', null=True, blank=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Detection on {self.camera.name} at {self.timestamp}"

    class Meta:
        verbose_name = 'Detection'
        verbose_name_plural = 'Detections'
        ordering = ['-timestamp']

class Recording(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='recordings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recordings')
    file = models.FileField(upload_to='recordings/')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    detected_faces = models.ManyToManyField(Face, blank=True, related_name='recordings')

    def __str__(self):
        return f"Recording from {self.camera.name} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = 'Recording'
        verbose_name_plural = 'Recordings'
        ordering = ['-start_time']

def record_camera(camera):
    # Build stream URL from camera fields
    stream_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/"
    cap = cv2.VideoCapture(stream_url)
    # Set up video writer, file path, etc.
    # Loop: read frames, write to file, run face detection if enabled
    # On stop: save Recording entry

class Command(BaseCommand):
    help = 'Start recording for all active cameras'

    def handle(self, *args, **options):
        cameras = Camera.objects.filter(is_active=True)
        for camera in cameras:
            t = threading.Thread(target=record_camera, args=(camera,))
            t.daemon = True
            t.start()
        self.stdout.write(self.style.SUCCESS('Started recording for all active cameras.'))
