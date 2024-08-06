from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from ..models.catagory import Category
from ..models.product import Product

def filter_product_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.all()
    product_list = []

    for product in products:
        if product.category == category:
            data = {
                'name': product.name,
                'id': product.id,
                'description': product.description,
                'picture': product.picture.url,
                'price': product.price,
            }
            product_list.append(data)
    

    print(product_list)

    return JsonResponse({'products': product_list}, safe=False)