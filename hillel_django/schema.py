import traceback
from rest_framework import serializers
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from django.contrib.auth.models import User
from products.models import Product, Category, Order, OrderProduct
from products.serializers import CategorySerializer, OrderSerializer
from graphql import GraphQLError

from graphene_django.forms.mutation import DjangoModelFormMutation


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'products']
        interfaces = (relay.Node, )


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )
        fields = (
            'id',
            'name',
        )


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    coca_cola = graphene.Field(ProductNode)

    def resolve_coca_cola(self, info):
        return Product.objects.get(name__icontains='Coca-Cola')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderProductType(DjangoObjectType):
    class Meta:
        model = OrderProduct
class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class ProductMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        description = graphene.String(required=False, default_value="")

    # The class attributes define the response of the mutation
    product = graphene.Field(ProductType)

    # Validate data before creating a book
    @classmethod
    def validate(cls, name: str, price: float):
        if not name:
            raise Exception("Name is required")
        if not price:
            raise Exception("Price is required")

    @classmethod
    def mutate(cls, root, info, name, price, description=None):
        try:
            print("running mutation")
            cls.validate(name, price)

            product = Product.objects.create(
                name=name,
                price=price,
                description=description,
            )
        except Exception as e:
            traceback.print_exc()

            return ProductMutation(product=None)

        return ProductMutation(product=product)


class CategoryMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


class OrderProductMutation(graphene.Mutation):

    class Arguments:
        order_id = graphene.Int(required=True)
        product_id =graphene.Int(required=True)
        quantity = graphene.Int(required=True)

    order_products = graphene.Field(OrderProductType)

    @classmethod
    def mutate(cls, root, info, order_id, product_id, quantity):
        order_products = OrderProduct.objects.create(
            order = Order.objects.get(id=order_id),
            product = Product.objects.get(id=product_id),
            quantity = quantity or 1
        )

        return OrderProductMutation(order_products=order_products)

# class OrderMutation(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.Int(required=True)
#         products = graphene.List(graphene.Int, required=True)
#
#     order = graphene.Field(OrderType)
#
#     @classmethod
#     def mutate(cls, root, info, user_id, products):
#         order = Order.objects.create(
#             user=user_id,
#             products=products
#         )
#
#         return OrderMutation(order=order)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class UserType(DjangoObjectType):
    class Meta:
        model = User


class OrderMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        products = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def validate_order(cls, user_id, products):
        if not user_id:
            raise Exception("User_id is required")
        if not products:
            raise Exception("Products are required")
    @classmethod
    def mutate(cls, root, info, user_id, products):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLEror("User not found")
        order = Order.objects.create(user=user)
        if not products:
            raise GraphQLError("You should provide at least one product")
        for product_id in products:
            try:
                product = Product.objects.get(pk=product_id)
                OrderProduct.objects.create(order=order, product=product)
            except Product.DoesNotExist:
                raise GraphQLError("Product does not exists")

        return OrderMutation(order=order)



class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_category = CategoryMutation.Field()
    create_order_product = OrderProductMutation.Field()
    create_order = OrderMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
