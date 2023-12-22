import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from products.models import Product, Category


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


schema = graphene.Schema(query=Query)
