from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import SignUpForm, ProfileEditForm, LoginForm
from activity.utils import log_activity
from cms.models import SiteSettings


class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        site_settings = SiteSettings.load()
        if site_settings.login_method not in ('both', 'password_only'):
            messages.error(request, 'Password login is currently disabled by the administrator. Please use facial login.')
            return redirect('biometric_facial_login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['login_method'] = 'password'
        if 'face_verified' in self.request.session:
            del self.request.session['face_verified']
        log_activity(self.request, 'login', description='Password login')
        return response


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['login_method'] = 'password'
            messages.success(request, 'Account created! Now enroll your face for secure authentication.')
            log_activity(request, 'create', model_name='User', object_id=user.id, description=f'User signed up: {user.username}')
            return redirect(reverse('biometric_enrollment') + '?next=' + reverse('product_list'))
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def custom_logout(request):
    log_activity(request, 'logout', description='User logged out')
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('product_list')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            log_activity(request, 'update', model_name='User', object_id=request.user.id, description='Profile updated')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
