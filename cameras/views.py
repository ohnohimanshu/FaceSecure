from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Camera
from .forms import CameraForm
from django.http import StreamingHttpResponse
import cv2
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CameraSerializer

@login_required
def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            cam = form.save(commit=False)
            cam.user = request.user
            cam.save()
            return redirect('dashboard')
    else:
        form = CameraForm()
    return render(request, 'add_camera.html', {'form': form})

@login_required
def generate(ip):
    cap = cv2.VideoCapture(ip)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@login_required
def live_feed(request, camera_id):
    cam = Camera.objects.get(id=camera_id, user=request.user)
    return StreamingHttpResponse(generate(cam.ip_address),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

@login_required
def edit_camera(request, camera_id):
    camera = Camera.objects.get(id=camera_id, user=request.user)
    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CameraForm(instance=camera)
    return render(request, 'edit_camera.html', {'form': form, 'camera': camera})

@login_required
def delete_camera(request, camera_id):
    camera = Camera.objects.get(id=camera_id, user=request.user)
    if request.method == 'POST':
        camera.delete()
        return redirect('dashboard')
    return render(request, 'delete_camera.html', {'camera': camera})

class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'ip_address']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Camera.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        camera = self.get_object()
        camera.is_active = not camera.is_active
        camera.save()
        return Response({'status': 'camera status toggled'})