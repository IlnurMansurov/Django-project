from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")
        users = User.objects.values_list('username', flat=True)
        for user in users:
            print(user)

        product_values = Product.objects.values('pk','name')
        for p_value in product_values:
            print(p_value)

        self.stdout.write("Done")