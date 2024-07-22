from django.contrib import admin
from users.models import CustomUser, CustomerProfile, SellerProfile
from .models.catagory import Category
from .models.product import Product, Color, Size
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models.order import Cart, Order, OrderForm

model_classes = {
    'product': Product,
    'category': Category,
    'color': Color
}

class CustomUserAdmin(UserAdmin):
    actions = ['update_user_permissions']

    def update_user_permissions(self, request, queryset):
        content_type = ContentType.objects.get_for_models(*model_classes.values())
        content_type_ids = [ct.id for ct in content_type.values()]

        # Filter permissions based on content types
        permissions_to_grant = Permission.objects.filter(content_type__id__in=content_type_ids)

        for user in queryset:
            if user.is_staff:
                # Clear existing permissions and grant new ones
                user.user_permissions.clear()
                user.user_permissions.add(*permissions_to_grant)
            else:
                # Remove all permissions if not staff
                user.user_permissions.clear()

        self.message_user(request, "User permissions updated successfully.")

    update_user_permissions.short_description = "Update user permissions"


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('order_display', 'user', 'product')

    def order_display(self, obj):
        return str(obj)
    order_display.short_description = 'Order'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomerProfile)
admin.site.register(SellerProfile)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Order, OrderAdmin)