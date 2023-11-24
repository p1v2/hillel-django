from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

<<<<<<< HEAD
=======
    def ready(self):
        from products.signals import order_created
>>>>>>> bfce55ba05055fae692f5cc7886977d8a20d4fec
