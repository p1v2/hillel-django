from datetime import datetime

from django.core.cache import cache
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.filters import ProductFilter
from products.models import Product as Product, Category, Order
from products.permissions import IsOwnerOrSuperAdmin
from products.serializers import (
    ProductSerializer,
    ProductViewSerializer,
    CategoryWithProductsSerializer,
    OrderSerializer,
)


class CacheResponseMixin:
    def list(self, request, *args, **kwargs):
        cache_key = f"{request.path}-list-{dict(request.query_params)}"
        print(cache_key)

        cached_data = cache.get(cache_key)

        if cached_data:
            print("From cache")
            return Response(cached_data)
        else:
            print("From DB")
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=3600)
            return response


class ProductViewSet(CacheResponseMixin, ModelViewSet):
    # foreign key - select_related
    # many to many - prefetch_related
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter

    # All different ways to paginate
    pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination
    # pagination_class = CursorPagination

    ordering_fields = ("name", "price")
    ordering = ("name",)

    permission_classes = ()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductViewSerializer
        else:
            return ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().prefetch_related("products")
    serializer_class = CategoryWithProductsSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrSuperAdmin,
    )
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=self.request.user)
