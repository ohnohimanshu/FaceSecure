from django.urls import path
from .views import add_camera, live_feed, edit_camera, delete_camera

urlpatterns = [
    path('add/', add_camera, name='add_camera'),
    path('edit/<int:camera_id>/', edit_camera, name='edit_camera'),
    path('delete/<int:camera_id>/', delete_camera, name='delete_camera'),
    path('live/<int:camera_id>/', live_feed, name='live_feed'),
]