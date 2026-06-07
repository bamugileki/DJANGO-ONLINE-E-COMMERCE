from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-created')

    return render(request, 'products/list.html', {
        'category': category,
        'products': products,
        'categories': categories,
        'query': query,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    avg_rating = product.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
    reviews = product.reviews.filter(is_approved=True)[:10]
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            from .models import ProductReview
            review, created = ProductReview.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            if created:
                messages.success(request, 'Review submitted! Awaiting approval.')
            else:
                messages.info(request, 'You have already reviewed this product.')
    
    return render(request, 'products/detail.html', {
        'product': product,
        'avg_rating': avg_rating,
        'reviews': reviews,
        'related_products': related_products,
    })
