from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils.timezone import now
from django.apps import apps
from django.forms import modelform_factory
from django.db.models import FileField, ImageField, ManyToManyField
from accounts.decorators import role_required
from accounts.models import UserProfile
from products.models import Product, Category
from orders.models import Order, OrderItem
from vendor.models import Vendor
from django.contrib.auth.models import User
from .model_registry import MODEL_REGISTRY, APP_ICONS


@login_required
@role_required('admin', 'manager')
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(paid=True).aggregate(Sum('items__price'))['items__price__sum'] or 0
    total_vendors = Vendor.objects.count()
    pending_vendors = Vendor.objects.filter(is_approved=False).count()
    recent_orders = Order.objects.select_related('user').order_by('-created')[:10]
    low_stock_products = Product.objects.filter(stock__lt=5, available=True)[:10]
    vendors = Vendor.objects.all()[:10]

    apps_data = _build_apps_data()

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_vendors': total_vendors,
        'pending_vendors': pending_vendors,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'vendors': vendors,
        'apps_data': apps_data,
        'APP_ICONS': APP_ICONS,
    })


@login_required
@role_required('admin', 'manager')
def vendor_approvals(request):
    vendors = Vendor.objects.filter(is_approved=False)
    return render(request, 'dashboard/vendor_approvals.html', {'vendors': vendors})


@login_required
@role_required('admin', 'manager')
def vendor_approve(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.is_approved = True
    vendor.is_active = True
    vendor.save()
    vendor.user.profile.role = 'vendor'
    vendor.user.profile.save()
    messages.success(request, f'{vendor.business_name} approved!')
    return redirect('vendor_approvals')


@login_required
@role_required('admin', 'manager')
def vendor_reject(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    messages.success(request, 'Vendor application rejected.')
    return redirect('vendor_approvals')


@login_required
@role_required('admin', 'manager', 'vendor')
def manage_users(request):
    users = User.objects.select_related('profile').all()

    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(profile__role=role_filter)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    active_count = users.filter(is_active=True).count()
    new_this_month = users.filter(date_joined__month=now().month, date_joined__year=now().year).count()

    return render(request, 'dashboard/manage_users.html', {
        'users': users,
        'role_filter': role_filter,
        'search_query': search_query,
        'active_count': active_count,
        'new_this_month': new_this_month,
    })


@login_required
@role_required('admin', 'manager')
def set_user_password(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if not password or len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        else:
            target.set_password(password)
            target.save()
            messages.success(request, f'Password for {target.username} updated successfully.')
            return redirect('manage_users')
    return render(request, 'dashboard/set_password.html', {'target': target})


@login_required
@role_required('admin', 'manager')
def manage_employees(request):
    from accounts.models import EmployeeProfile
    employees = EmployeeProfile.objects.select_related('user').all()
    return render(request, 'dashboard/manage_employees.html', {'employees': employees})


def _get_model(app_label, model_name):
    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        return None


def _get_registry_key(app_label, model_name):
    return f'{app_label}.{model_name}'


def _build_apps_data(current_app=None, current_model=None):
    data = {}
    for key, meta in MODEL_REGISTRY.items():
        app_label = key.split('.')[0]
        mn = key.split('.')[1]
        data.setdefault(app_label, []).append({
            'key': key,
            'name': meta['name'],
            'icon': meta['icon'],
            'model_name': mn,
            'active': app_label == current_app and mn == current_model,
        })
    return dict(sorted(data.items()))


@login_required
@role_required('admin', 'manager')
def model_list(request, app_label, model_name):
    model = _get_model(app_label, model_name)
    key = _get_registry_key(app_label, model_name)
    meta = MODEL_REGISTRY.get(key)
    if not model or not meta:
        messages.error(request, 'Model not found.')
        return redirect('admin_dashboard')

    queryset = model.objects.all()
    search_query = request.GET.get('q', '')
    if search_query and meta['fields']:
        first_field = meta['fields'][0]
        filter_kwargs = {f'{first_field}__icontains': search_query}
        try:
            queryset = queryset.filter(**filter_kwargs)
        except Exception:
            pass

    objects = queryset

    apps_data = _build_apps_data(current_app=app_label, current_model=model_name)

    return render(request, 'dashboard/model_list.html', {
        'model': model,
        'meta': meta,
        'objects': objects,
        'app_label': app_label,
        'model_name': model_name,
        'apps_data': apps_data,
        'APP_ICONS': APP_ICONS,
        'search_query': search_query,
    })


@login_required
@role_required('admin', 'manager')
def model_add(request, app_label, model_name):
    model = _get_model(app_label, model_name)
    key = _get_registry_key(app_label, model_name)
    meta = MODEL_REGISTRY.get(key)
    if not model or not meta:
        messages.error(request, 'Model not found.')
        return redirect('admin_dashboard')

    exclude_fields = ['id']
    form_class = modelform_factory(model, exclude=exclude_fields)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'{meta["name"]} created successfully.')
            return redirect('model_list', app_label=app_label, model_name=model_name)
    else:
        form = form_class()

    apps_data = _build_apps_data()

    return render(request, 'dashboard/model_form.html', {
        'model': model,
        'meta': meta,
        'form': form,
        'app_label': app_label,
        'model_name': model_name,
        'apps_data': apps_data,
        'is_edit': False,
        'APP_ICONS': APP_ICONS,
    })


@login_required
@role_required('admin', 'manager')
def model_edit(request, app_label, model_name, pk):
    model = _get_model(app_label, model_name)
    key = _get_registry_key(app_label, model_name)
    meta = MODEL_REGISTRY.get(key)
    if not model or not meta:
        messages.error(request, 'Model not found.')
        return redirect('admin_dashboard')

    obj = get_object_or_404(model, pk=pk)
    exclude_fields = ['id']
    form_class = modelform_factory(model, exclude=exclude_fields)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'{meta["name"]} updated successfully.')
            return redirect('model_list', app_label=app_label, model_name=model_name)
    else:
        form = form_class(instance=obj)

    apps_data = _build_apps_data()

    return render(request, 'dashboard/model_form.html', {
        'model': model,
        'meta': meta,
        'form': form,
        'object': obj,
        'app_label': app_label,
        'model_name': model_name,
        'apps_data': apps_data,
        'is_edit': True,
        'APP_ICONS': APP_ICONS,
    })


@login_required
@role_required('admin', 'manager')
def model_delete(request, app_label, model_name, pk):
    model = _get_model(app_label, model_name)
    key = _get_registry_key(app_label, model_name)
    meta = MODEL_REGISTRY.get(key)
    if not model or not meta:
        messages.error(request, 'Model not found.')
        return redirect('admin_dashboard')

    obj = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, f'{meta["name"]} deleted successfully.')
        return redirect('model_list', app_label=app_label, model_name=model_name)

    apps_data = _build_apps_data()

    return render(request, 'dashboard/model_confirm_delete.html', {
        'model': model,
        'meta': meta,
        'object': obj,
        'app_label': app_label,
        'model_name': model_name,
        'apps_data': apps_data,
        'APP_ICONS': APP_ICONS,
    })
