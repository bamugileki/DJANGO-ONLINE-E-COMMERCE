import base64
import io
import json
import math
import os
import pickle

import cv2
import face_recognition
import numpy as np
from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import FaceDescriptor
from cms.models import SiteSettings

User = get_user_model()

try:
    from ultralytics import YOLO
    model_path = os.path.join(settings.BASE_DIR, 'biometric', 'Liveness_detection_models', 'best.pt')
    liveness_model = YOLO(model_path)
    liveness_classNames = ["fake", "real"]
except Exception as e:
    liveness_model = None
    print(f"Warning: Failed to load YOLO Liveness model: {e}")


def _liveness_check(img):
    if liveness_model is None:
        return True
    results = liveness_model(img, stream=False, verbose=False)
    for r in results:
        for box in r.boxes:
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            if conf > 0.8 and liveness_classNames[cls] == 'real':
                return True
    return False


def _ensure_8bit_rgb(img):
    if img is None or img.size == 0:
        return None
    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    channels = 1 if len(img.shape) == 2 else img.shape[2]
    if channels == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif channels == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img


def _get_encoding_from_image(img):
    img = _ensure_8bit_rgb(img)
    if img is None:
        return None
    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        return None
    encodings = face_recognition.face_encodings(img, face_locations)
    return encodings[0] if encodings else None


def _decode_image(request):
    data = json.loads(request.body)
    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(img_bytes))
    return np.array(img.convert('RGB'))


@login_required
def enrollment(request):
    has_face = hasattr(request.user, 'face_descriptor') and request.user.face_descriptor.is_active
    next_url = request.GET.get('next', '')
    return render(request, 'biometric/enrollment.html', {'has_face': has_face, 'next_url': next_url})


@csrf_exempt
@login_required
def save_face_descriptor(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)
    try:
        img = _decode_image(request)
        # if not _liveness_check(img):
        #     return JsonResponse({'status': 'error', 'message': 'Liveness verification failed. Access denied.'})
        encoding = _get_encoding_from_image(img)
        if encoding is None:
            return JsonResponse({'status': 'error', 'message': 'No face detected in the image.'})
        encoded_bytes = base64.b64encode(pickle.dumps(encoding)).decode('ascii')
        FaceDescriptor.objects.update_or_create(
            user=request.user,
            defaults={'embedding': encoded_bytes, 'is_active': True}
        )
        return JsonResponse({'status': 'ok', 'message': 'Face enrolled successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def verify_face(request):
    has_face = hasattr(request.user, 'face_descriptor') and request.user.face_descriptor.is_active
    if not has_face:
        messages.warning(request, 'No face enrolled. Please enroll first.')
        return redirect('biometric_enrollment')
    next_url = request.GET.get('next', '/')
    return render(request, 'biometric/verify.html', {'next_url': next_url})


@csrf_exempt
@login_required
def verify_face_descriptor(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)
    try:
        img = _decode_image(request)
        # if not _liveness_check(img):
        #     return JsonResponse({'status': 'error', 'message': 'Liveness verification failed.'})
        live_encoding = _get_encoding_from_image(img)
        if live_encoding is None:
            return JsonResponse({'status': 'error', 'message': 'No face detected.'})
        stored = getattr(request.user, 'face_descriptor', None)
        if not stored or not stored.is_active:
            return JsonResponse({'status': 'error', 'message': 'No face enrolled.'})
        stored_encoding = pickle.loads(base64.b64decode(stored.embedding))
        matches = face_recognition.compare_faces([stored_encoding], live_encoding)
        face_distance = face_recognition.face_distance([stored_encoding], live_encoding)
        if matches[0]:
            similarity = 1 - face_distance[0]
            request.session['face_verified'] = True
            return JsonResponse({'status': 'ok', 'similarity': round(similarity, 4)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Face does not match', 'similarity': round(1 - face_distance[0], 4)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def facial_login(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    settings = SiteSettings.load()
    if not settings.facial_login_enabled:
        messages.error(request, 'Facial login is currently disabled by the administrator.')
        return redirect('login')
    return render(request, 'biometric/facial_login.html')


@csrf_exempt
def facial_login_verify(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)
    try:
        img = _decode_image(request)
        # if not _liveness_check(img):
        #     return JsonResponse({'status': 'error', 'message': 'Liveness verification failed. Access denied.'})
        live_encoding = _get_encoding_from_image(img)
        if live_encoding is None:
            return JsonResponse({'status': 'error', 'message': 'No face detected.'})
        descriptors = FaceDescriptor.objects.filter(is_active=True).select_related('user')
        if not descriptors.exists():
            return JsonResponse({'status': 'error', 'message': 'No registered faces found. Please sign up first.'})
        for desc in descriptors:
            stored_encoding = pickle.loads(base64.b64decode(desc.embedding))
            matches = face_recognition.compare_faces([stored_encoding], live_encoding)
            if matches[0]:
                user = desc.user
                auth_login(request, user)
                request.session['face_verified'] = True
                return JsonResponse({
                    'status': 'ok',
                    'redirect': '/',
                    'username': user.username
                })
        return JsonResponse({'status': 'error', 'message': 'Face does not match any registered user.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
