import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.cart import Cart
from orders.models import Order, OrderItem


@login_required
def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('product_list')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            postal_code=request.POST['postal_code'],
            city=request.POST['city'],
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'tzs',
                    'product_data': {'name': item['product'].name},
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            } for item in cart],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout_success', args=[order.id])),
            cancel_url=request.build_absolute_uri(reverse('checkout_cancel')),
        )
        order.stripe_id = session.id
        order.save()
        return redirect(session.url, code=303)

    return render(request, 'checkout/checkout.html', {'cart': cart})


@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = Cart(request)
    cart.clear()
    order.paid = True
    order.save()
    return render(request, 'checkout/success.html', {'order': order})


def checkout_cancel(request):
    return render(request, 'checkout/cancel.html')
