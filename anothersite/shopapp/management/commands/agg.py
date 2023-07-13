from typing import Sequence

from django.core.management import BaseCommand
from django.db.models import Avg, Max, Min, Count, Sum
from shopapp.models import Order
from django.contrib.auth.models import User

class Command(BaseCommand):
     def handle(self, *args, **options):
         self.stdout.write("Start demo select aggregate")

         orders = Order.objects.annotate(
             total=Sum('products__price'),
             products_count=Count('products'),
         )
         for order in orders:
             print(
                 f'Order #{order.id} '
                 f'with {order.products_count} '
                 f'products worth {order.total}'
             )
         self.stdout.write("Done")

    #     result = Product.objects.aggregate(
    #         Avg('price'),
    #         Max('price'),
    #         Min('price'),
    #         Count('price'),
    #     )
    #
    #     print(result)
