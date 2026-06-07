from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Address
from vendor.models import Vendor


class Command(BaseCommand):
    help = 'Seed database with manager, vendor, and customer accounts'

    def handle(self, *args, **options):
        users_data = [
            {
                'role': 'manager',
                'first_name': 'John', 'last_name': 'Mwanga',
                'username': 'manager_john',
                'email': 'john.manager@mimicmeshop.com',
                'password': 'Mgr@12345',
            },
            {
                'role': 'vendor',
                'first_name': 'Amina', 'last_name': 'Hassan',
                'username': 'vendor_amina',
                'email': 'amina.vendor@mimicmeshop.com',
                'password': 'Vnd@12345',
                'store_name': 'Amina Fashion Hub',
            },
            {
                'role': 'vendor',
                'first_name': 'Peter', 'last_name': 'Mushi',
                'username': 'vendor_peter',
                'email': 'peter.vendor@mimicmeshop.com',
                'password': 'Vnd@54321',
                'store_name': 'Mushi Electronics',
            },
            {
                'role': 'customer',
                'first_name': 'Fatima', 'last_name': 'Ali',
                'username': 'fatima_ali',
                'email': 'fatima.customer@mimicmeshop.com',
                'password': 'Cust@12345',
                'phone': '+255689045666',
            },
            {
                'role': 'customer',
                'first_name': 'James', 'last_name': 'Robert',
                'username': 'james_robert',
                'email': 'james.customer@mimicmeshop.com',
                'password': 'Cust@54321',
                'phone': '+255689045666',
            },
            {
                'role': 'customer',
                'first_name': 'Neema', 'last_name': 'John',
                'username': 'neema_john',
                'email': 'neema.customer@mimicmeshop.com',
                'password': 'Cust@11223',
                'phone': '+255689045666',
            },
        ]

        for data in users_data:
            role = data.pop('role')
            store_name = data.pop('store_name', None)
            phone = data.pop('phone', '')

            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                },
            )
            if created:
                user.set_password(data['password'])
                user.save()

            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': role, 'phone': phone},
            )
            if not created and profile.role != role:
                profile.role = role
                profile.phone = phone
                profile.save()

            if role == 'vendor' and store_name:
                Vendor.objects.get_or_create(
                    user=user,
                    defaults={
                        'business_name': store_name,
                        'is_approved': True,
                        'business_email': data['email'],
                        'phone': phone or '+255689045666',
                        'address': 'Default Address',
                        'city': 'Dar es Salaam',
                    },
                )

            if role == 'customer':
                Address.objects.get_or_create(
                    user=user,
                    address_type='shipping',
                    defaults={
                        'first_name': data['first_name'],
                        'last_name': data['last_name'],
                        'phone': phone or '+255689045666',
                        'address_line1': 'Default Address',
                        'city': 'Dar es Salaam',
                        'state': 'Dar es Salaam',
                        'postal_code': '00000',
                        'country': 'Tanzania',
                        'is_default': True,
                    },
                )

            status = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f'{status}: {data["username"]} ({role})'))

        self.stdout.write(self.style.SUCCESS('\nAll accounts seeded successfully!'))
