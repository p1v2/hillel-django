from django.contrib import admin
from django.db import models

from products.models import Product, Category, Tag, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "order_products__product")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ("name", "price", "category", "tags")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("category")

    actions = ["mark_discount"]

    list_display = ("name", "price")

    list_editable = ("price",)

    list_filter = ("category",)

    ordering = ("name",)

    def mark_discount(self, request, queryset):
        for element in queryset:
            element.price = element.price * 0.9
            element.name = f"discounted {element.name}"
            element.save()
