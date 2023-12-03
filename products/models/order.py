from django.db import models


class Order(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    products = models.ManyToManyField(
        "products.Product", through="products.OrderProduct"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        total = 0
        for order_product in self.order_products.all():
            total += order_product.product.price * order_product.quantity
        return total

    @property
    def bill(self):
        to_print = ""
        to_pay = 0

        for order_product in self.order_products.all():
            product_to_pay = order_product.product.price * \
                             order_product.quantity
            to_print += f"{order_product.product.name} - " \
                        f"{order_product.quantity} - " \
                        f"{round(product_to_pay)}\n"
            to_pay += product_to_pay

        to_print += f"Total: {round(to_pay)}"

        return to_print
