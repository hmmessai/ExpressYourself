from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from ..models.catagory import Category
from ..models.product import Product

def filter_product_by_category(request, category_id):
    product_list = []

    if category_id == 0:
        products = Product.objects.all()
        for product in products:
            data = {
                'name': product.name,
                'id': product.id,
                'description': product.description,
                'picture': product.picture.url,
                'price': int(product.price),
            }
            product_list.append(data)
    else:
        category = Category.objects.get(id=category_id)
        products = Product.objects.all()

        for product in products:
            if product.category == category:
                data = {
                    'name': product.name,
                    'id': product.id,
                    'description': product.description,
                    'picture': product.picture.url,
                    'price': int(product.price),
                }
                product_list.append(data)

    print(product_list)

    return JsonResponse({'products': product_list}, safe=False)