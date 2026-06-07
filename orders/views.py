from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})
