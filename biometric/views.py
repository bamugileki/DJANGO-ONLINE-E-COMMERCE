import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FaceDescriptor


@login_required
def enrollment(request):
    has_face = hasattr(request.user, 'face_descriptor') and request.user.face_descriptor.is_active
    return render(request, 'biometric/enrollment.html', {'has_face': has_face})


@csrf_exempt
@login_required
def save_face_descriptor(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)
    try:
        data = json.loads(request.body)
        descriptor = data.get('descriptor', '')
        if not descriptor:
            return JsonResponse({'status': 'error', 'message': 'No descriptor provided'}, status=400)
        FaceDescriptor.objects.update_or_create(
            user=request.user,
            defaults={'embedding': descriptor, 'is_active': True}
        )
        messages.success(request, 'Face enrolled successfully.')
        return JsonResponse({'status': 'ok'})
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
        data = json.loads(request.body)
        live_descriptor = data.get('descriptor', '')
        stored = getattr(request.user, 'face_descriptor', None)
        if not stored or not stored.is_active:
            return JsonResponse({'status': 'error', 'message': 'No face enrolled'}, status=400)
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, stored.embedding, live_descriptor).ratio()
        threshold = float(data.get('threshold', 0.85))
        if similarity >= threshold:
            request.session['face_verified'] = True
            return JsonResponse({'status': 'ok', 'similarity': round(similarity, 4)})
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Face does not match',
                'similarity': round(similarity, 4)
            }, status=403)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
