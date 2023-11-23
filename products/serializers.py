from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from products.models import Product, Category, Tag, Market, StoreInventory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'category', 'tags')


class ProductViewSerializer(ProductSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)


class CategoryWithProductsSerializer(CategorySerializer):
    products = ProductSerializer(many=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ('products',)

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('__all__')

class StoreInventorySerializer(serializers.ModelSerializer):
    market = MarketSerializer()
    product = ProductSerializer()
    class Meta:
        model = StoreInventory
        fields = ('__all__')

class RegistrationSerializer(ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('username', 'password', 'token')

