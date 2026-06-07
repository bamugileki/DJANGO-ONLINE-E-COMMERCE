import os, shutil, re
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from products.models import Category, Brand, Product, ProductImage


IMAGES_DIR = settings.BASE_DIR / 'images'
MEDIA_PRODUCTS = settings.MEDIA_ROOT / 'products'


class Command(BaseCommand):
    help = 'Seed products from images directory'

    def handle(self, *args, **options):
        os.makedirs(MEDIA_PRODUCTS, exist_ok=True)

        clothing = Category.objects.get_or_create(name='Clothing', defaults={'slug': 'clothing'})[0]
        electronics = Category.objects.get_or_create(name='Electronics', defaults={'slug': 'electronics'})[0]
        beauty = Category.objects.get_or_create(name='Beauty & Health', defaults={'slug': 'beauty-health'})[0]
        home = Category.objects.get_or_create(name='Home & Kitchen', defaults={'slug': 'home-kitchen'})[0]

        brands = {
            'PremiumWear': Brand.objects.get_or_create(name='PremiumWear', defaults={'slug': 'premiumwear'})[0],
            'Apple': Brand.objects.get_or_create(name='Apple', defaults={'slug': 'apple'})[0],
            'Samsung': Brand.objects.get_or_create(name='Samsung', defaults={'slug': 'samsung'})[0],
            'Sony': Brand.objects.get_or_create(name='Sony', defaults={'slug': 'sony'})[0],
            'GlowLab': Brand.objects.get_or_create(name='GlowLab', defaults={'slug': 'glowlab'})[0],
            'HomeChef': Brand.objects.get_or_create(name='HomeChef', defaults={'slug': 'homechef'})[0],
        }

        products_data = [
            {
                'name': 'Premium Cotton T-Shirt',
                'category': clothing, 'brand': brands['PremiumWear'],
                'description': 'Soft, breathable 100% organic cotton t-shirt with a modern fit. Perfect for casual wear.',
                'price': 29.99, 'stock': 150,
            },
            {
                'name': 'Classic Denim Jacket',
                'category': clothing, 'brand': brands['PremiumWear'],
                'description': 'Timeless denim jacket crafted from premium denim. Features a comfortable regular fit and classic button closure.',
                'price': 89.99, 'stock': 75,
            },
            {
                'name': 'iPhone 15 Pro Max',
                'category': electronics, 'brand': brands['Apple'],
                'description': 'Apple\'s flagship smartphone with A17 Pro chip, 48MP camera system, and titanium design.',
                'price': 1199.99, 'stock': 50,
            },
            {
                'name': 'MacBook Air M3',
                'category': electronics, 'brand': brands['Apple'],
                'description': 'Ultra-thin laptop powered by the M3 chip. 15.3-inch Liquid Retina display, 18-hour battery life.',
                'price': 1299.99, 'stock': 30,
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'category': electronics, 'brand': brands['Samsung'],
                'description': 'Samsung\'s premium smartphone with built-in S Pen, 200MP camera, and Galaxy AI features.',
                'price': 1099.99, 'stock': 40,
            },
            {
                'name': 'Sony WH-1000XM5 Headphones',
                'category': electronics, 'brand': brands['Sony'],
                'description': 'Industry-leading noise cancellation with premium sound quality. 30-hour battery life with quick charging.',
                'price': 349.99, 'stock': 60,
            },
            {
                'name': 'Smart LED TV 55 inch',
                'category': electronics, 'brand': brands['Samsung'],
                'description': 'Stunning 4K UHD Smart LED TV with vibrant colors, built-in streaming apps, and voice control.',
                'price': 499.99, 'stock': 25,
            },
            {
                'name': 'Professional Hair Dryer',
                'category': beauty, 'brand': brands['GlowLab'],
                'description': 'High-performance hair dryer with ionic technology, multiple heat settings, and concentrator nozzle.',
                'price': 79.99, 'stock': 100,
            },
            {
                'name': 'Organic Vitamin C Serum',
                'category': beauty, 'brand': brands['GlowLab'],
                'description': 'Brightening vitamin C serum with hyaluronic acid and vitamin E. Promotes radiant, youthful skin.',
                'price': 34.99, 'stock': 200,
            },
            {
                'name': 'Stainless Steel Cookware Set',
                'category': home, 'brand': brands['HomeChef'],
                'description': '10-piece professional stainless steel cookware set. Includes pots, pans, and lids with tempered glass.',
                'price': 199.99, 'stock': 45,
            },
        ]

        for data in products_data:
            image_name = f'{data["name"]}.jpg'
            src = IMAGES_DIR / image_name
            dest = MEDIA_PRODUCTS / image_name

            if src.exists():
                shutil.copy2(src, dest)
                self.stdout.write(self.style.SUCCESS(f'  Copied: {image_name}'))

            base_slug = slugify(data['name'])
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'slug': slug,
                    'category': data['category'],
                    'brand': data['brand'],
                    'description': data['description'],
                    'price': data['price'],
                    'stock': data['stock'],
                    'image': f'products/{image_name}',
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {data["name"]}'))
            else:
                self.stdout.write(f'Exists: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\nAll {Product.objects.count()} products seeded!'))
