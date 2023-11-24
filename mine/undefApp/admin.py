from django.contrib import admin
from undefApp.models import Tag, Product, Order, OrderProduct, Category, Store, StoreInventory

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Store)
admin.site.register(StoreInventory)