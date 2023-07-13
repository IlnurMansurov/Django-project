from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk ations")

        result = Product.objects.filter(
            name__contains='Smart',
        ).update(discount=10)

        print(result)

        # info = [
        #     ('Smartfone 1', 199,),
        #     ('Smartfone 2', 1939,),
        #     ('Smartfone 3', 1299,),
        #     ('Smartfone 4', 1991,),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)
        #
        # for object in result:
        #     print(object)


        self.stdout.write("Done")