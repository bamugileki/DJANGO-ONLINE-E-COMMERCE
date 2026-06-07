from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Product, ProductReview


class Command(BaseCommand):
    help = 'Seed product reviews from existing customers'

    def handle(self, *args, **kwargs):
        customers = User.objects.filter(profile__role='customer')
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR('No products found'))
            return

        reviews_data = [
            {'user': 'fatima_ali', 'product': 'Premium Cotton T-Shirt', 'rating': 5, 'comment': 'Great quality cotton, very comfortable and fits perfectly. Will definitely buy more!'},
            {'user': 'fatima_ali', 'product': 'Organic Vitamin C Serum', 'rating': 4, 'comment': 'My skin feels brighter after two weeks. A bit pricey but worth it.'},
            {'user': 'james_robert', 'product': 'iPhone 15 Pro Max', 'rating': 5, 'comment': 'Amazing phone! The camera is incredible and battery lasts all day.'},
            {'user': 'james_robert', 'product': 'Sony WH-1000XM5 Headphones', 'rating': 5, 'comment': 'Best noise cancellation I have ever experienced. Perfect for travel and work.'},
            {'user': 'james_robert', 'product': 'Smart LED TV 55 inch', 'rating': 4, 'comment': 'Great picture quality for the price. Smart features work smoothly.'},
            {'user': 'neema_john', 'product': 'Classic Denim Jacket', 'rating': 5, 'comment': 'Absolutely love this jacket! The fit is perfect and the material is high quality.'},
            {'user': 'neema_john', 'product': 'Professional Hair Dryer', 'rating': 4, 'comment': 'Dries hair very fast without causing damage. Multiple heat settings are useful.'},
            {'user': 'neema_john', 'product': 'Stainless Steel Cookware Set', 'rating': 5, 'comment': 'Excellent cookware set. Heats evenly and looks beautiful in my kitchen.'},
            {'user': 'admin', 'product': 'MacBook Air M3', 'rating': 5, 'comment': 'Incredibly fast and lightweight. The battery life is outstanding for a full work day.'},
            {'user': 'admin', 'product': 'Samsung Galaxy S24 Ultra', 'rating': 4, 'comment': 'Great Android alternative with an amazing display. The S Pen is a nice bonus.'},
        ]

        created = 0
        for entry in reviews_data:
            try:
                user = User.objects.get(username=entry['user'])
                product = Product.objects.get(name=entry['product'])
            except (User.DoesNotExist, Product.DoesNotExist):
                continue
            _, was_created = ProductReview.objects.update_or_create(
                product=product,
                user=user,
                defaults={
                    'rating': entry['rating'],
                    'comment': entry['comment'],
                    'is_approved': True,
                }
            )
            if was_created:
                created += 1
                self.stdout.write(f'  Added: {user.username} → {product.name} ({entry["rating"]}/5)')

        self.stdout.write(self.style.SUCCESS(f'\n{created} reviews created'))
