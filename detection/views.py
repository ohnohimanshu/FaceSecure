from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cameras.models import Camera
from faces.models import Face
from .stream import process_camera as old_process_camera
from threading import Thread
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Detection, Recording
from .serializers import DetectionSerializer, DetectionCreateSerializer
import threading
from .utils import process_camera
from django.utils import timezone
from django.db.models import Q

@login_required
def start_streams(request):
    user = request.user
    cameras = Camera.objects.filter(user=user)
    faces = Face.objects.filter(user=user)
    recent_detections = Detection.objects.filter(
        camera__user=user
    ).order_by('-timestamp')[:10]  # Get last 10 detections
    
    for cam in cameras:
        Thread(target=old_process_camera, args=(cam, user)).start()
    
    return render(request, 'dashboard.html', {
        'cameras': cameras,
        'faces': faces,
        'recent_detections': recent_detections
    })

@login_required
def delete_recording(request, recording_id):
    recording = Recording.objects.get(id=recording_id, user=request.user)
    if request.method == 'POST':
        recording.delete()
        return redirect('recordings_list')
    return render(request, 'delete_recording.html', {'recording': recording})

@login_required
def recordings_list(request):
    recordings = Recording.objects.filter(user=request.user)
    camera_id = request.GET.get('camera')
    date = request.GET.get('date')
    if camera_id:
        recordings = recordings.filter(camera_id=camera_id)
    if date:
        try:
            date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            recordings = recordings.filter(start_time__date=date_obj)
        except Exception:
            pass
    recordings = recordings.order_by('-start_time')
    cameras = Camera.objects.filter(user=request.user)
    return render(request, 'recordings_list.html', {'recordings': recordings, 'cameras': cameras, 'selected_camera': camera_id, 'selected_date': date})

class DetectionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'notification_sent']
    search_fields = ['camera__name', 'detected_face__name']
    ordering_fields = ['timestamp', 'confidence_score']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Detection.objects.filter(camera__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return DetectionCreateSerializer
        return DetectionSerializer

    @action(detail=False, methods=['post'])
    def start_detection(self, request):
        cameras = request.user.cameras.filter(is_active=True)
        if not cameras.exists():
            return Response(
                {'error': 'No active cameras found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        for camera in cameras:
            thread = threading.Thread(target=process_camera, args=(camera, request.user))
            thread.start()
        return Response({
            'status': 'Detection started',
            'cameras_count': cameras.count()
        })