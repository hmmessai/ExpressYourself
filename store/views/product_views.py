import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models.product import Product, Color, Size
from store.models.order import Order, Cart, Payment
from store.models.catagory import Category
from django.contrib import messages

@login_required
def product(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, 'store/products/products_admin.html', {'product': product})


@login_required
def add_product(request):
    colors = Color.objects.all()
    sizes = Size.objects.all()
    category = Category.objects.all()
    if request.method == 'POST':
        try:
            colors = Color.objects.filter(id__in=request.POST.getlist('color'))
            sizes = Size.objects.filter(id__in=request.POST.getlist('size'))
            category = request.POST.get('category')

            product = Product.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                category=Category.objects.get(id=category),
                rating=request.POST.get('rating'),
                status='available',
                posted_by=request.user,
            )

            product.available_colors.set(colors)
            product.size.set(sizes)
            product.save()
            print(product.order_count)
            messages.success(request, f"Successfully added Product {request.POST.get('name')}")
        except Exception as e:
            messages.error(request, f"Error Occured: {e}")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return redirect('home')
    return render(request, 'store/products/add_product.html', {'colors': colors, 'sizes': sizes, 'category': category})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product:
        product.delete()
    else:
        return redirect.back()
    return redirect('home')

def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    uorders = Order.objects.filter(user=order.user)
    if order:
        return render(request, 'store/products/order_details.html', {'order': order, 'uorders': uorders})
    else:
        return redirect.back()
