from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from users.models import CustomUser
from store.models.product import Product, Category
from .models import Request

@receiver(post_save, sender=CustomUser)
def grant_staff_permissions(sender, instance, created, **kwargs):
    if instance.is_staff:
        content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            instance.user_permissions.add(permission)


@receiver(post_save, sender=Request)
def create_request(sender, instance, created, **kwargs):
    if created:
        category = Category.objects.get_or_create(name='Requested')
        product = Product.objects.create(category=category[0], posted_by=instance.requester.user, status='requested')
        instance.product = product
        instance.save()
