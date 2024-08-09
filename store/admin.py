from django.contrib import admin
from .models.catagory import Category
from .models.product import Product, Color, Size
from .models.order import Cart, Order, OrderForm



class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order_count')
    fields = ('name', 'description', 'price', 'category', 'available_colors', 'rating', 'size', 'picture', 'status', 'posted_by')

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('order_display', 'user', 'product')

    def order_display(self, obj):
        return str(obj)
    order_display.short_description = 'Order'

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Order, OrderAdmin)