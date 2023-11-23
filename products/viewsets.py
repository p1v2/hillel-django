from rest_framework.authentication import BasicAuthentication
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from hillel_django.authentication import MyCustomAuthentication
from products.models import Product as Product, Category, Market, StoreInventory
from rest_framework.permissions import IsAuthenticated
from products.serializers import ProductSerializer, ProductViewSerializer, CategoryWithProductsSerializer,StoreInventorySerializer,MarketSerializer


class ProductViewSet(ModelViewSet):
    # foreign key - select_related
    # many to many - prefetch_related
    queryset = Product.objects.all().select_related('category').prefetch_related('tags')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductViewSerializer
        else:
            return ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().prefetch_related('products')
    serializer_class = CategoryWithProductsSerializer

class MarketViewSet(ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class StoreInventoryViewSet(ModelViewSet):
    queryset = StoreInventory.objects.all()
    serializer_class = StoreInventorySerializer