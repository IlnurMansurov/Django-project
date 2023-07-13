from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User
from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products

# def save_csv_orders(file, encoding):
#     csv_file = TextIOWrapper(
#         file,
#         encoding=encoding,
#     )
#     reader = DictReader(csv_file)
#
#     orders = [
#         Order(**row)
#         for row in reader
#     ]
#     Order.objects.bulk_create(orders)
#     return orders
# def save_csv_orders(file, encoding):
#     csv_file = TextIOWrapper(
#         file,
#         encoding=encoding,
#     )
#     reader = DictReader(csv_file)
#
#     orders = [
#         Order(
#             delivery_address=row['delivery_address'],
#             promocode=row['promocode'],
#             user=User.objects.get(id=row['user']),
#             products=row['products']
#         )
#         for row in reader
#     ]
#
#     return orders
def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    orders = []
    for row in reader:

        product_ids = [int(id) for id in row['products'].split(',')]
        products = Product.objects.filter(id__in=product_ids)
        order = Order(
            delivery_address=row['delivery_address'],
            promocode=row['promocode'],
            user=User.objects.get(id=row['user'])
        )
        order.save()
        order.products.set(products)
        order.save()
        orders.append(order)
    return orders