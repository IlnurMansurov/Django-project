from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page
from .views import (
    GroupListView,
    OrdersListView,
    ProductCreateView,
    OrderCreateView,
    ShopIndexView,
    ProductListViews,
    ProductDetailsView,
    OrderDetailView,
    ProductUpdateView,
    ProductDeleteView,
    OrderDeleteView,
    OrderUpdateView,
    ProductsDataExportView,
    OrdersDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    UserOrdersExport,

)


app_name = 'shopapp'
routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('api/', include(routers.urls)),
    path("", ShopIndexView.as_view(), name='Index'),
    path("groups/", GroupListView.as_view(), name="groups_list"),
    path("products/", ProductListViews.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("products/export", ProductsDataExportView.as_view(), name="products_export"),
    path("orders/export", OrdersDataExportView.as_view(), name="orders_export"),
    path("products/latest/feed/", LatestProductsFeed(), name="products-latest"),
    path('user/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders'),
    path("users/<int:user_id>/orders/export/", UserOrdersExport.as_view(), name='user_orders_export'),
]
