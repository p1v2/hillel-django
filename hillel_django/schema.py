import traceback

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation

from products.models import Product, Category, Order, OrderProduct
from products.serializers import CategorySerializer

from django.db import transaction


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


class OrderInput(graphene.InputObjectType):
    products = graphene.List(graphene.ID, required=True)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'products',
            'total_price',
            'bill',
        )


class CreateOrder(graphene.Mutation):
    class Arguments:
        order_input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def __init__(self, order):
        self.order = order

    @staticmethod
    def mutate(root, info, order_input):
        if not order_input.products:
            raise Exception('An order must contain at least one product.')

        with transaction.atomic():
            order = Order.objects.create()
            order_products = []

        for product_id in order_input.products:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise Exception(f'Product with id {product_id} does not exist.')

            order_products.append(OrderProduct(order=order, product=product))

        OrderProduct.objects.bulk_create(order_products)
        order.save()

        return CreateOrder(order=order)


class CategoryMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_category = CategoryMutation.Field()
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
