# Create your models here.
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from products.models.category import Category
from products.models.tag import Tag

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os


def non_negative_validator(value):
    if value <= 0:
        raise ValidationError("Price cannot be negative.")


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(validators=[non_negative_validator])
    description = models.TextField(blank=True)
    # models.CASCADE - if category is deleted,
    # all products in this category will be deleted
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, related_name="products"
    )
    # models.SET_NULL - if category is deleted,
    # all products in this category will be set to NULL
    # models.RESTRICT - don't allow to delete
    # category if there are products in this category
    # models.DO_NOTHING - don't do anything if category is deleted
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)

    image = models.ImageField(upload_to="products", null=True, blank=True)

    orders = models.ManyToManyField(
        "products.Order", through="products.OrderProduct"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Compless image to 200x200 (convert to JPEG)
        if self.image:
            image = Image.open(self.image)
            image.thumbnail((200, 200))

            thumb_name, thumb_extension = os.path.splitext(self.image.name)

            thumb_filename = thumb_name + "_thumb" + ".jpg"

            temp_thumb = BytesIO()
            image.convert("RGB").save(temp_thumb, format='JPEG')
            temp_thumb.seek(0)

            # set save=False, otherwise it will run in an infinite loop
            self.image.save(thumb_filename,
                            SimpleUploadedFile(
                                thumb_filename,
                                temp_thumb.read(),
                                content_type=f"image/jpeg",
                            ),
                            save=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Signal after creating product
@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    cache_keys = "/api/products/-list*"
    cache.delete_pattern(cache_keys)
    print("cache cleared")

    if created:
        print(f"{sender} {instance.name} was created")
    else:
        print(f"{sender} {instance.name} was updated")


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    cache_keys = "/api/products/-list*"
    cache.delete_pattern(cache_keys)
    print("cache cleared")

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    print(f"{sender} {instance.name} is about to be saved")


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    print(f"{sender} {instance.name} was saved")


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    print(f"{sender} {instance.name} was deleted")
