from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models.catagory import Category
from ..models.product import Product

@login_required
def filter_product_by_category(request, category_id):
    product_list = []

    # If the category is set to all it sends 0 as the category id
    # so we will return all the products without considering thier 
    # category.
    if category_id == 0:
        products = Product.objects.all()
        for product in products:
            if product.status == 'available':
                data = {
                    'name': product.name,
                    'id': product.id,
                    'description': product.description,
                    'picture': product.picture.url,
                    'price': int(product.price),
                }
                product_list.append(data)
    # if the category is set we will filter products based on their category
    else:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category, status='available')

        for product in products:
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


@login_required
def filter_product_by_rating(request):
    product_list = []
    products = Product.objects.filter(rating=5)

    for product in products:
        data = {
            'name': product.name,
            'id': product.id,
            'description': product.description,
            'picture': product.picture.url,
            'price': int(product.price),
        }
        product_list.append(data)

    return JsonResponse({'products': product_list}, safe=False)