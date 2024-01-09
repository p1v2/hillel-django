import traceback

import graphene
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation

from products.models import Product, Category,Order,OrderProduct
from products.serializers import CategorySerializer


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

class OrderProductType(DjangoObjectType):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('products',)

    products = graphene.List(OrderProductType)

    def resolve_products(value_obj, info):
        return value_obj.order_products.all()


class OrderProductIn(graphene.InputObjectType):
    product_id = graphene.Int()
    quantity = graphene.Float()


class OrderMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        products = graphene.List(OrderProductIn, required=True)
        # The class attributes define the response of the mutation
        order = graphene.Field(OrderType)

    # Validate data before creating a order
    @classmethod
    def validate(cls, info, products: list,order:list):
        if not products:
            raise Exception("Products are required")
        if not len(products):
            raise Exception("At least a single product is required")
        if not order:
            raise Exception("order are required")

    @classmethod
    def mutate(cls, root, info, products,order):
        try:
            cls.validate(info, products,order)
            order = Order.objects.create(
                user_id=info.context.user.id,
            )
            OrderProduct.objects.bulk_create([
                OrderProduct(
                    order=order,
                    product_id=max(p.product_id, 0),
                    quantity=max(p.quantity, 0),  # Ensure quantity is non-negative
                )
                for p in products
                if p.quantity >= 0 # Add a check for non-negative quantity
                if p.product_id >= 0 # Add a check for non-negative quantity
            ])
        except IntegrityError as integrity_error:
            # Обработка нарушения целостности базы данных (например, уникальное ограничение)
            traceback.print_exc()
            return OrderMutation(order=None)

        except ValidationError as validation_error:
            # Обработка ошибки проверки (вам может потребоваться определить ValidationError)
            traceback.print_exc()
            return OrderMutation(order=None)

        except Exception as e:
            # Обработка других конкретных исключений при необходимости
            traceback.print_exc()
            return OrderMutation(order=None)

        return OrderMutation(order=order)


class CategoryMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_category = CategoryMutation.Field()
    create_order = OrderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
