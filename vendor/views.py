from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from products.models import Product, Category, ProductImage, ProductVariation
from orders.models import Order, OrderItem
from .models import Vendor, VendorPayout, Withdrawal


def vendor_apply(request):
    if request.user.is_authenticated and hasattr(request.user, 'vendor_profile'):
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        is_new_user = not request.user.is_authenticated
        if is_new_user:
            from accounts.forms import SignUpForm
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
            else:
                return render(request, 'vendor/apply.html', {'form': form})
        else:
            user = request.user

        vendor_data = {
            'user': user,
            'business_name': request.POST.get('business_name'),
            'business_type': request.POST.get('business_type', 'individual'),
            'business_email': request.POST.get('business_email'),
            'phone': request.POST.get('phone'),
            'registration_number': request.POST.get('registration_number', ''),
            'tax_id': request.POST.get('tax_id', ''),
            'address': request.POST.get('address', ''),
            'city': request.POST.get('city', ''),
            'country': request.POST.get('country', 'Tanzania'),
            'description': request.POST.get('description', ''),
            'bank_name': request.POST.get('bank_name', ''),
            'account_name': request.POST.get('account_name', ''),
            'account_number': request.POST.get('account_number', ''),
            'mobile_money_number': request.POST.get('mobile_money_number', ''),
            'payment_preference': request.POST.get('payment_preference', 'mobile_money'),
        }
        vendor = Vendor.objects.create(**vendor_data)
        for field in ['logo', 'national_id_image', 'business_license_image', 'tax_certificate']:
            if request.FILES.get(field):
                setattr(vendor, field, request.FILES[field])
        vendor.save()
        user.profile.role = 'vendor'
        user.profile.save()
        messages.success(request, 'Your vendor application has been submitted for review!')
        return redirect('product_list')
    return render(request, 'vendor/apply.html')


@login_required
def vendor_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return redirect('vendor_apply')
    total_products = Product.objects.filter(vendor=vendor).count()
    total_orders = OrderItem.objects.filter(product__vendor=vendor).values('order').distinct().count()
    total_revenue = vendor.total_earnings
    recent_orders = OrderItem.objects.filter(product__vendor=vendor).select_related('order', 'product')[:10]
    return render(request, 'vendor/dashboard.html', {
        'vendor': vendor,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'section': 'dashboard',
    })


@login_required
def vendor_products(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'vendor/products.html', {
        'vendor': vendor,
        'products': products,
        'section': 'products',
    })


@login_required
def vendor_product_add(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        category = get_object_or_404(Category, id=category_id)
        import uuid
        product = Product.objects.create(
            vendor=vendor,
            category=category,
            name=name,
            slug=name.lower().replace(' ', '-') + '-' + str(uuid.uuid4())[:8],
            description=description,
            price=price,
            stock=stock,
        )
        if request.FILES.get('image'):
            product.image = request.FILES['image']
            product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('vendor_products')
    return render(request, 'vendor/product_form.html', {
        'vendor': vendor,
        'categories': categories,
        'section': 'products',
    })


@login_required
def vendor_product_edit(request, product_id):
    vendor = get_object_or_404(Vendor, user=request.user)
    product = get_object_or_404(Product, id=product_id, vendor=vendor)
    categories = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')
        product.available = request.POST.get('available') == 'on'
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('vendor_products')
    return render(request, 'vendor/product_form.html', {
        'vendor': vendor,
        'product': product,
        'categories': categories,
        'section': 'products',
    })


@login_required
def vendor_product_delete(request, product_id):
    vendor = get_object_or_404(Vendor, user=request.user)
    product = get_object_or_404(Product, id=product_id, vendor=vendor)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('vendor_products')


@login_required
def vendor_orders(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    order_items = OrderItem.objects.filter(product__vendor=vendor).select_related('order', 'product')
    return render(request, 'vendor/orders.html', {
        'vendor': vendor,
        'order_items': order_items,
        'section': 'orders',
    })


@login_required
def vendor_earnings(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    payouts = VendorPayout.objects.filter(vendor=vendor)
    withdrawals = Withdrawal.objects.filter(vendor=vendor)
    return render(request, 'vendor/earnings.html', {
        'vendor': vendor,
        'payouts': payouts,
        'withdrawals': withdrawals,
        'section': 'earnings',
    })


@login_required
def vendor_withdrawal_request(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        payment_details = request.POST.get('payment_details')
        if vendor.available_balance >= float(amount):
            Withdrawal.objects.create(
                vendor=vendor,
                amount=amount,
                payment_method=payment_method,
                payment_details=payment_details,
            )
            vendor.available_balance -= float(amount)
            vendor.save()
            messages.success(request, 'Withdrawal request submitted!')
        else:
            messages.error(request, 'Insufficient balance!')
        return redirect('vendor_earnings')
    return redirect('vendor_earnings')


@login_required
def vendor_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        vendor.business_name = request.POST.get('business_name')
        vendor.business_email = request.POST.get('business_email')
        vendor.phone = request.POST.get('phone')
        vendor.address = request.POST.get('address')
        vendor.city = request.POST.get('city')
        vendor.description = request.POST.get('description')
        if request.FILES.get('logo'):
            vendor.logo = request.FILES['logo']
        vendor.save()
        messages.success(request, 'Profile updated!')
        return redirect('vendor_profile')
    return render(request, 'vendor/profile.html', {
        'vendor': vendor,
        'section': 'profile',
    })
