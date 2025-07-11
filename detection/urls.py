from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DetectionViewSet, recordings_list, delete_recording

router = DefaultRouter()
router.register(r'', DetectionViewSet, basename='detection')

urlpatterns = [
    path('recordings/', recordings_list, name='recordings_list'),
    path('recordings/delete/<int:recording_id>/', delete_recording, name='delete_recording'),
    path('', include(router.urls)),
]