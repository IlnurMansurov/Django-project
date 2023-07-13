from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices
from django.conf import settings
from shopapp.models import Product, Order
from django.contrib.auth.models import Permission

class ProductCreateViewTestCase(TestCase):
    def setUp(self) ->None:

        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                "name": self.product_name,
                "price": '1200',
                "description": "SUPER TABLET",
                "discount": '10',


            }
            , HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):

        cls.product = Product.objects.create(name='Sosiski')
    @classmethod
    def tearDownClass(cls):
        cls.product.delete()


    def test_get_product_(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk':self.product.pk})
            , HTTP_USER_AGENT='Mozilla/5.0')

        self.assertEquals(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
            , HTTP_USER_AGENT='Mozilla/5.0')

        self.assertContains(response, self.product.name)

class OrderListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='myQA', password='123456')
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEquals(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products_export'),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEquals(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'arhved': product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEquals(
            products_data['products'],
            expected_data,
        )

class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):

        cls.user = User.objects.create_user(username='myQA', password='123456')
        cls.order = Order.objects.create(
            delivery_address='some street',
            promocode='supa',
            user=cls.user
        )


    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.user.delete()



    def setUp(self):
        self.client.force_login(self.user)
        permission = Permission.objects.get(codename='view_order')
        self.user.user_permissions.add(permission)

    def test_get_order(self):
        response = self.client.get(
            reverse('shopapp:order_details', kwargs={'pk': self.order.pk}),
            HTTP_USER_AGENT='Mozilla/5.0'
        )

        self.assertEquals(response.status_code, 200)

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:order_details', kwargs={'pk': self.order.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)

        order = response.context['order']
        self.assertEquals(order.pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]
    @classmethod
    def setUpClass(cls):

        cls.user = User.objects.create_user(username='myQA', password='123456')
        cls.user.is_staff = True
        cls.user.save()



    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


    def setUp(self):
        self.client.force_login(self.user)


    def test_get_orders_view(self):
        response = self.client.get(
            reverse('shopapp:orders_export'),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': str(order.user),
                'products': str(order.products),
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expected_data,
        )
