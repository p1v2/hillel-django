from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from products.models import Product, Category, Tag, Order, OrderProduct, Store, StoreInventory
from products.tasks import order_created_task


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


class RegistrationSerializer(ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('username', 'password', 'token')


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_products')

    def create(self, validated_data):
        order_products = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)

        order_products_items = []
        for order_product in order_products:
            order_products_items.append(OrderProduct(order=order, **order_product))

        OrderProduct.objects.bulk_create(order_products_items)

        return order


class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = ('product', 'quantity')