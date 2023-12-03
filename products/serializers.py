from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from products.models import Product, Category, Tag, Order, OrderProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "description", "category", "tags")


class ProductViewSerializer(ProductSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)


class CategoryWithProductsSerializer(CategorySerializer):
    products = ProductSerializer(many=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ("products",)


class RegistrationSerializer(ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ("username", "password", "token")


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ("product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products_count = serializers.SerializerMethodField(read_only=True)

    # Validate at least one order_product
    def validate(self, attrs):
        if len(attrs["order_products"]) == 0:
            raise serializers.ValidationError(
                "You must specify at least one product")
        return attrs

    def get_products_count(self, order):
        return order.order_products.count()

    class Meta:
        model = Order
        fields = ("id", "user", "order_products", "products_count", "created_at")

    def create(self, validated_data):
        order_products = validated_data.pop("order_products")
        order = Order.objects.create(**validated_data)

        order_products_items = []
        for order_product in order_products:
            order_products_items.append(
                OrderProduct(order=order, **order_product)
            )

        OrderProduct.objects.bulk_create(order_products_items)

        return order
