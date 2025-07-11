import os
import threading
import cv2
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from cameras.models import Camera
from detection.models import Recording
from django.contrib.auth import get_user_model

# Optional: import your face detection logic here
# from detection.utils import detect_faces

RECORDINGS_DIR = os.path.join(settings.MEDIA_ROOT, 'recordings')
os.makedirs(RECORDINGS_DIR, exist_ok=True)


def record_camera(camera):
    # Build stream URL (adjust as needed for your camera type)
    if camera.username and camera.password:
        stream_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/"
    else:
        stream_url = f"rtsp://{camera.ip_address}:{camera.port}/"
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print(f"Failed to open stream for camera {camera}")
        return
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    start_time = datetime.datetime.now()
    filename = f"{camera.id}_{start_time.strftime('%Y%m%d_%H%M%S')}.avi"
    filepath = os.path.join(RECORDINGS_DIR, filename)
    out = cv2.VideoWriter(filepath, fourcc, 20.0, (640, 480))
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Optionally run face detection
            if camera.face_detection_enabled:
                # faces = detect_faces(frame)
                pass  # Add your face detection logic here
            out.write(frame)
            frame_count += 1
            # For demo: record only 10 seconds (200 frames at 20fps)
            if frame_count >= 200:
                break
    finally:
        cap.release()
        out.release()
        end_time = datetime.datetime.now()
        # Save Recording entry
        Recording.objects.create(
            camera=camera,
            user=camera.user,
            file=f"recordings/{filename}",
            start_time=start_time,
            end_time=end_time
        )
        print(f"Saved recording for camera {camera}")


class Command(BaseCommand):
    help = 'Start recording for all active cameras'

    def handle(self, *args, **options):
        cameras = Camera.objects.filter(is_active=True)
        for camera in cameras:
            t = threading.Thread(target=record_camera, args=(camera,))
            t.daemon = True
            t.start()
        self.stdout.write(self.style.SUCCESS('Started recording for all active cameras.'))
        # Keep the main thread alive
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('Stopping camera recording threads.') 