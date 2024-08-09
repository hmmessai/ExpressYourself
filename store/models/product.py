from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .catagory import Category
from users.models import CustomUser
from datetime import datetime
import os




RATINGS = [
    (1, '1'),
    (2, '2'),
    (3, '3'), 
    (4, '4'), 
    (5, '5')
    ]

class Size(models.Model):
    name = models.CharField(max_length=50, null=False)
    short_letter = models.CharField(max_length=2, null=False)

    def __str__(self) -> str:
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=15, null=False)
    hex_value = models.CharField(max_length=7)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, default=0.00, decimal_places=2, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name='products')
    available_colors = models.ManyToManyField(Color, related_name='using_products')
    rating = models.IntegerField(choices=RATINGS, null=True)
    size = models.ManyToManyField(Size, blank=True)
    picture = models.ImageField(upload_to='product_images/', default='product_images/istockphoto-1159447883-612x612.jpg', blank=True, null=True)
    status = models.CharField(max_length=20, null=False, default='available')
    order_count = models.IntegerField(null=False, default=0)
    posted_by = models.ForeignKey(
        CustomUser, 
        limit_choices_to={'is_staff': True},
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='products_posted')


    def __str__(self) -> str:
        return self.name
    

@receiver(pre_save, sender=Product)
def delete_related_photos_on_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Product.objects.get(pk=instance.pk)
        
        if old_instance.status != instance.status and instance.status == "unavailable":
            if old_instance.picture and old_instance.picture.name != 'product_images/istockphoto-1159447883-612x612.jpg':
                photo_path = os.path.join(settings.MEDIA_ROOT, instance.picture.name)
                print(os.path.exists(photo_path))
                if os.path.exists(photo_path):
                    os.remove(photo_path)

