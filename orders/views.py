from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Order


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def receipt_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, paid=True)
    return render(request, 'orders/receipt.html', {'order': order})
