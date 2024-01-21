import traceback

from rest_framework import serializers

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types import InputObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from django.contrib.auth.models import User

from products.models import Product, Category, Order, OrderProduct
from products.serializers import CategorySerializer, OrderSerializer, OrderProductSerializer

'''Input schemas'''
class OrderProductInput(InputObjectType):
    product_id = graphene.Int()
    quantity = graphene.Float()


'''Types'''
class OrderProductType(DjangoObjectType):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('products', )

    products = graphene.List(OrderProductType)
    
    def resolve_products(value_obj, info):
        return value_obj.order_products.all()


# class UserType(DjangoObjectType):
#     class Meta:
#         model = User
#         exclude = ('password',  )



'''Nodes'''
# class UserNode(DjangoObjectType):
#     class Meta:
#         model = User
#         filter_fields = {'username': ['exact'],}
#         interfaces = (relay.Node, )
#         fields = (
#             'username',
#             'first_name',
#             'last_name'
#         )


# class OrderProductNode(DjangoObjectType):
#     class Meta:
#         model = OrderProduct
#         interfaces = (relay.Node, )
#         fields = (
#             'order',
#             'product',
#             'quantity'
#         )


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

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'products']
        interfaces = (relay.Node, )

# class OrderNode(DjangoObjectType):
#     class Meta:
#         model = Order
#         filter_fields = {
#             'products__name': ['exact', 'icontains', 'istartswith']
#         }
#         interfaces = (relay.Node, )

'''Mutations'''
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
        # try:
            # print("running mutation")
            cls.validate(name, price)

            product = Product.objects.create(
                name=name,
                price=price,
                description=description or "",
                )
            # print(product.name, product.price, product.description)
        # except Exception as e:
        #     traceback.print_exc()
        #     return ProductMutation(product=None)
            return ProductMutation(product=product)





class OrderMutation(graphene.Mutation):
    # print('please work')
    class Arguments:
        # print('arguments')
        # username = graphene.String(required=True)

        products = graphene.List(OrderProductInput, required=True)

    #returning field
    order = graphene.Field(OrderType)


    @classmethod
    def validate(cls, products, order):
        print('validation')
        if not products:
            raise Exception('Products are required')

        for product in products:
            if not product['product']:
                raise Exception("Valid product_id is required")

            if not product['quantity'] or product['quantity'] < 0:
                raise Exception("Valid quantity is required")


    @classmethod
    def mutate(cls, root, info, products):
        # print('mutation')
        
        try:
            # print("running mutation")
            
            cls.validate(info, products)
            
            # print('PreCreate')
            order = Order.objects.create(user_id=info.context.user.id)
            OrderProduct.objects.bulk_create([
                OrderProduct(order=order,
                             product_id=product.product_id,
                             quantity=product.quantity)
                for product in products])
            # print('Created yay')

        except Exception as e:
            # print('exception')
            traceback.print_exc()
            return OrderMutation(order=None)
        return OrderMutation(order=order)


class CategoryMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


'''Main Query'''
class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    coca_cola = graphene.Field(ProductNode)

    def resolve_coca_cola(self, info):
        return Product.objects.get(name__icontains='Coca-Cola')


'''Main Mutation'''
class Mutation(graphene.ObjectType):
    create_product = ProductMutation.Field()
    create_category = CategoryMutation.Field()
    create_order = OrderMutation.Field()


'''Schema'''
schema = graphene.Schema(query=Query, mutation=Mutation)
