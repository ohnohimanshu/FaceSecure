# FaceSecure - Face Recognition Security System

FaceSecure is a Django-based SaaS application that uses IP cameras and face recognition to detect known individuals and send alerts via email. The system provides a RESTful API for managing cameras, faces, and detection processes.

## Features

- JWT Authentication
- Camera Management (Add, List, Update, Delete)
- Face Management (Upload, List, Update, Delete)
- Real-time Face Detection
- Email Notifications
- RESTful API
- User Management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ohnohimanshu/FaceSecure.git
cd FaceSecure
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add:
```
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get user details
- `PUT /api/auth/change-password/` - Change password

### Cameras
- `GET /api/cameras/` - List all cameras
- `POST /api/cameras/` - Add a new camera
- `GET /api/cameras/{id}/` - Get camera details
- `PUT /api/cameras/{id}/` - Update camera
- `DELETE /api/cameras/{id}/` - Delete camera
- `POST /api/cameras/{id}/toggle_active/` - Toggle camera status

### Faces
- `GET /api/faces/` - List all faces
- `POST /api/faces/` - Add a new face
- `GET /api/faces/{id}/` - Get face details
- `PUT /api/faces/{id}/` - Update face
- `DELETE /api/faces/{id}/` - Delete face
- `POST /api/faces/{id}/toggle_active/` - Toggle face status

### Detection
- `GET /api/detection/` - List all detections
- `POST /api/detection/` - Create a new detection
- `GET /api/detection/{id}/` - Get detection details
- `POST /api/detection/start_detection/` - Start face detection on all active cameras

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@facesecure.com or create an issue in the repository. 
