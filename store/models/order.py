from django.db import models
from decimal import Decimal
from .users import CustomUser
from .product import Product, Color, Size
from django import forms


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name='cart')
    
    def __str__(self) -> str:
        return f"{self.user.first_name}'s Cart"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='order_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, related_name='order_product')
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cart = models.ForeignKey(Cart, limit_choices_to={'user': user}, null=True, blank=True, related_name='orders', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.product_id:
            price = self.product.price + (Decimal(0.02) * self.product.price)
            self.total_price = price

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Order {self.user} - {self.product}"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'product', 'color', 'size']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                product = Product.objects.get(pk=product_id)
                self.fields['color'].queryset = product.available_colors.all()
                self.fields['size'].queryset = product.size.all()
            except (ValueError, Exception):
                pass
        elif self.instance and self.instance.product_id:
            self.fields['color'].queryset = self.instance.product.available_colors.all()
            self.fields['size'].queryset = self.instance.product.size.all()