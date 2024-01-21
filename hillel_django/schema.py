import traceback

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation

from products.models import Product, Category, OrderProduct, Order
from products.serializers import CategorySerializer


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'products']
        interfaces = (relay.Node,)


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node,)
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


class CategoryMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


class OrderType(DjangoObjectType):
    class Meta:
        model = OrderProduct


class OrderMutation(graphene.Mutation):
    class Arguments:
        product = graphene.ID(required=False)
        order = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def validate(cls, product, order, quantity: int):
        if not product:
            raise Exception("Name is required")
        if not order:
            raise Exception("Price is required")
        if not quantity:
            raise Exception('quantity is required')

    @classmethod
    def mutate(cls, root, info, product, order, quantity):
        try:
            print("running mutation")
            cls.validate(product, order, quantity)
            order_instance = Order.objects.get(id=order)
            product_instance = Product.objects.get(id=product)

            order = OrderProduct.objects.create(
                product=product_instance,
                order=order_instance,
                quantity=quantity,
            )
        except Exception as e:
            traceback.print_exc()

            return OrderMutation(order=None)

        return OrderMutation(order=order)


class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_category = CategoryMutation.Field()
    create_order = OrderMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
