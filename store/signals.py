from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from users.models import CustomUser
from .models.product import Product, Category

@receiver(post_save, sender=CustomUser)
def grant_staff_permissions(sender, instance, created, **kwargs):
    if instance.is_staff:
        content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            instance.user_permissions.add(permission)
