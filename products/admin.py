from django.contrib import admin

from products.models import Product, Category, Tag, Order, Store, StoreInventory

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Store)
admin.site.register(StoreInventory)
