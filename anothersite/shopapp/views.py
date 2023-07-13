"""
Модуль содерждит различные наборы представлений.

View интернет-магазина: по товарам, заказам и т.д.

"""
import logging
from timeit import default_timer
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from csv import DictWriter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from .forms import ProductForm,  GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.request import Request
from .common import save_csv_products
from django.contrib.gis.feeds import Feed
from django.core.cache import cache


log = logging.getLogger(__name__)
@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        'name',
        'description',
    ]
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = [
        'pk',
        'price',
    ]
    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
         return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content='text/csv')
        filename = 'product-export.csv'
        response['content-Disposition'] = f'attachment; filename ={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response
    @action(
        detail=False,
        methods=['post'],
        parser_classes=[MultiPartParser],

    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class LatestProductsFeed(Feed):
    title = 'Shop products(latest)'
    description = 'Updates on changes and addition shop products'
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return (
            Product.objects
            .filter(archived=False)
            .order_by('-created_at')[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]

    def item_link(self, item: Product):
        return reverse('shopapp:product_details', kwargs={'pk': item.pk})

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        'delivery_address',
        'products',
    ]
    filterset_fields = [
        'products',
        'delivery_address',
        'user',

    ]
    ordering_fields = [
        'pk',
        'user',
        'products'
    ]

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content='text/csv')
        filename = 'order-export.csv'
        response['content-Disposition'] = f'attachment; filename ={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [

            'delivery_address',
            'promocode',
            'user',
            'products',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        for order in queryset:
            writer.writerow({
                field: getattr(order, field)
                for field in fields
            })
        return response

    @action(
        detail=False,
        methods=['post'],
        parser_classes=[MultiPartParser],

    )
    def upload_csv(self, request: Request):
        orders = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class ShopIndexView(View):

    #@method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('laptop', 1999),
            ('dekstop', 2999),
            ('smartfone', 999),
        ]

        some_list = [
            '1st cycle elem',
            'second cycle elem',
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "some_list": some_list,
            'items': 4,
        }
        print('shop index context', context)
        log.debug('Products for shop index: %s', products)
        log.info('Rendering shop index')
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductListViews(ListView):
    template_name = 'shopapp/products-list.html'
    #model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)

    

class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')




class ProductUpdateView(PermissionRequiredMixin, UpdateView):

    permission_required = 'shopapp.change_product'
    model = Product
    #fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if self.request.user.has_perm('change_product'):
            raise PermissionDenied
        if obj.created_by != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return response

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrdersListView(LoginRequiredMixin,ListView):
    template_name = 'shopapp/order-list.html'
    model = Order
    context_object_name = 'orders'


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    template_name = 'shopapp/order-details.html'
    model = Order
    context_object_name = 'order'

class OrderCreateView(CreateView):
    model = Order
    fields = 'delivery_address', 'promocode', 'user', 'products'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_address', 'promocode', 'user', 'products'
    template_name_suffix = "_update_form"
    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )
class OrderDeleteView(DeleteView):

    model = Order
    success_url = reverse_lazy('shopapp:orders_list')

class ProductsDataExportView(View):
    def get(self, requests: HttpRequest) ->JsonResponse:
        cache_key = 'products_data_export'
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'arhved': product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        return JsonResponse({'products': products_data})


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, requests: HttpRequest) ->JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': str(order.user),
                'products': str(order.products),
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user_orders_list.html'

    def get_queryset(self, **kwargs):
        user_id = self.kwargs['user_id']
        self.owner = get_object_or_404(User, pk=user_id)
        return self.owner.order_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class UserOrdersExport(View):
    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        cache_key = f"user_orders:{user_id}"
        user_orders_data = cache.get(cache_key)

        if user_orders_data is None:
            owner = get_object_or_404(User, pk=user_id)
            orders = owner.order_set.order_by('pk').all()
            serializer = OrderSerializer(orders, many=True)
            user_orders_data = serializer.data
            cache.set(cache_key, user_orders_data, 300)

        return JsonResponse({'orders': user_orders_data})

