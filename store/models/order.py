from django.db import models
from django.core.files import File
from decimal import Decimal
from users.models import CustomUser
from .product import Product, Color, Size
from django import forms
from datetime import datetime
from utilities.qr import generate_qr_code


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
    done = models.BooleanField(null=False, default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    cart = models.ForeignKey(Cart, limit_choices_to={'user': user}, null=True, blank=True, related_name='orders', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}'s order for {self.product}"

    def save(self, *args, **kwargs):
        if self.product_id:
            price = Decimal(self.product.price) + (Decimal(0.02) * Decimal(str(self.product.price)))
            self.total_price = price
        
        buffer = generate_qr_code(self.__dict__)

        self.qr_code.save(f'{self}_qr.png', File(buffer), save=False)

        super(Order, self).save(*args, **kwargs)
        
        if not hasattr(self, 'payment'):
            Payment.objects.create(order=self)

    


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'product', 'color', 'size', 'done']
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


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    advance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, null=False, default='not done')

    def save(self, *args, **kwargs):
        if self.order_id:
            advance_payment = Decimal(0.5) * Decimal(self.order.total_price)
            self.advance = advance_payment

        super(Payment, self).save(*args, **kwargs)

    def payAdvance(self):
        pass

    def payInFull(self):
        pass

    def payRemainder(self):
        pass
        

    def __str__(self) -> str:
        return f"Payment for {self.order}"

