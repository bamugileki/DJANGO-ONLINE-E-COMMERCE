from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from .models import ContactMessage, ContactReply
from .forms import ContactForm
from notifications.models import Notification
from accounts.decorators import role_required


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.full_name = request.user.get_full_name() or request.user.username
                msg.email = request.user.email
            msg.save()

            admins = User.objects.filter(
                models.Q(profile__role='admin') | models.Q(is_superuser=True)
            ).distinct()
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='contact',
                    title=f'New Contact: {msg.subject}',
                    message=f'{msg.full_name} ({msg.email}) sent: {msg.message[:200]}',
                    link=reverse('support_contact_detail', args=[msg.id]),
                )

            try:
                send_mail(
                    subject=f'[SmartTrade Africa] New Contact: {msg.subject}',
                    message=f'From: {msg.full_name} ({msg.email})\n\n{msg.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, 'Your message has been sent. We will get back to you within 24 hours.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'cms/contact.html', {'form': form})


@login_required
@role_required('admin', 'manager', 'vendor')
def contact_list(request):
    user = request.user
    profile_role = getattr(getattr(user, 'profile', None), 'role', '')

    if profile_role == 'vendor':
        messages_list = ContactMessage.objects.filter(
            models.Q(category='vendor') | models.Q(category='payment')
        )
    else:
        messages_list = ContactMessage.objects.all()

    return render(request, 'support/contact_list.html', {'messages_list': messages_list})


@login_required
@role_required('admin', 'manager', 'vendor')
def contact_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    Notification.objects.filter(user=request.user, link=reverse('support_contact_detail', args=[pk]), is_read=False).update(is_read=True)

    if request.method == 'POST':
        reply_text = request.POST.get('message', '').strip()
        if reply_text:
            ContactReply.objects.create(
                contact=msg,
                user=request.user,
                message=reply_text,
            )
            msg.status = 'completed'
            msg.save()

            messages.success(request, 'Reply sent successfully.')
        return redirect('support_contact_detail', pk=pk)

    return render(request, 'support/contact_detail.html', {'msg': msg})
