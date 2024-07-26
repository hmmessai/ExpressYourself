from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Request
from store.models.product import Product, Category

@receiver(post_save, sender=Request)
def create_request(sender, instance, created, **kwargs):
    if created:
        category = Category.objects.get_or_create(name='Requested')
        product = Product.objects.create(category=category[0], posted_by=instance.requester.user, status='requested')
        instance.product = product
        instance.save()
