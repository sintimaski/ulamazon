import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djulam.settings')
django.setup()

from django.contrib.auth.models import User

from orders.models import Order, OrderItem
from products.models import Product

# Create some users
user1 = User.objects.create_user(id=2, username='user3', password='password2')
user2 = User.objects.create_user(id=3, username='user4', password='password2')

# Create some products
product1 = Product.objects.create(name='Product 1', price=20.0, user=user1)
product2 = Product.objects.create(name='Product 2', price=20.0, user=user1)
product3 = Product.objects.create(name='Product 3', price=20.0, user=user2)

# Create some orders
order1 = Order.objects.create(user=user1, address='123 Main St')
order2 = Order.objects.create(user=user2, address='456 Oak Rd')

# Add order items
OrderItem.objects.create(order=order1, product=product1, quantity=2)
OrderItem.objects.create(order=order1, product=product2, quantity=1)
OrderItem.objects.create(order=order2, product=product2, quantity=3)
OrderItem.objects.create(order=order2, product=product3, quantity=1)

print('Data populated successfully.')
