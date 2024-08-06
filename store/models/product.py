from django.db import models
from .catagory import Category
from users.models import CustomUser

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
    posted_by = models.ForeignKey(
        CustomUser, 
        limit_choices_to={'is_staff': True},
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='products_posted')


    def __str__(self) -> str:
        return self.name