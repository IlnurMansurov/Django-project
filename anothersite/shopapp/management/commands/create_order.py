from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create Order with products")
        user = User.objects.get(username='admin')
        products: Sequence[Product] = Product.objects.only('id').all()
        order, created = Order.objects.get_or_create(
            delivery_address='Ul ivanova kv8',
            promocode='Python5',
            user=user,
        )

        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")