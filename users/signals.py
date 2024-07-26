from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Request
from store.models.product import Product

@receiver(post_save, sender=Request)
def create_request(sender, instance, created, **kwargs):
    if created:
        product = Product.objects.create(posted_by=instance.requester.user, status='requested')
        instance.product = product
        instance.save()
