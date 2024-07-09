from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .models import CustomUser
from .models import Product, Category

@receiver(post_save, sender=CustomUser)
def grant_staff_permissions(sender, instance, created, **kwargs):
    if instance.is_staff:
        # Grant 'Can add product' permission
        content_type = ContentType.objects.get_for_model(Product)
        permission = Permission.objects.filter(content_type=content_type)
        for p in permission:
            instance.user_permissions.add(p)
