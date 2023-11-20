from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from products.models import Product, Category, Tag,Store,StoreInventory


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

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id',"name","number_of_employees","description","date_joined","address","job_title","phone_number")

class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = ('id',"name","store","description","product","quantity")



class StoreProductsSerializer(StoreSerializer):
    products = ProductSerializer(many=True)

    class Meta(StoreSerializer.Meta):
        fields = StoreSerializer.Meta.fields + ('products',)




class StoreInventorySerializerGET(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = StoreInventory
        fields = ('id', 'store', 'product', 'quantity', 'description','name')



class ProductViewSerializer(ProductSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)


class CategoryWithProductsSerializer(CategorySerializer):
    products = ProductSerializer(many=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ('products',)

class StoreProductsSerializer(StoreSerializer):
    products = ProductSerializer(many=True)

    class Meta(StoreSerializer.Meta):
        fields = StoreSerializer.Meta.fields + ('products',)


class RegistrationSerializer(ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('username', 'password', 'token')
