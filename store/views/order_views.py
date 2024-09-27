import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from store.models.product import Product, Color, Size
from store.models.order import Order, Cart, Payment
from utilities.qr import generate_qr_code, decode_qr_code

@login_required
def order(request, product_id, cart=None):
    product = Product.objects.get(id=product_id)
    user = request.user
    products = Product.objects.filter(category=product.category, status='available')
    if request.method == 'POST':
        try:
            color_name = request.POST['color'] 
            size_name = request.POST['size']
            
            color = Color.objects.get(name=color_name)
            size = Size.objects.get(name=size_name)

            order = Order.objects.create(user=user, product=product, color=color, size=size)
            if cart and not user.cart.orders.filter(product=product).exists():
                print(cart)
                print(user.cart)
                order.cart = user.cart
            payment = Payment.objects.create()
            payment.orders.add(order)
            payment.save()
            order.save()
            return redirect('payment_with_order', order_id=order.id)
        except Exception as e:
             print(e)
             return render(request, 'store/order.html', {'product': product, 'products': products, 'messages': ["Select color and size before ordering."]})

    return render(request, 'store/order.html', {'product': product, 'products': products})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    if request.method == 'POST':
        try:
            cart, created = Cart.objects.get_or_create(user=user)
            if cart.product.filter(id=product_id).exists():
                raise Exception("Order already added to cart")
            cart.product.add(product)
            messages.success(request, f"Successfully added to cart")
        except Exception as e:
            messages.error(request, f"Error Occured: {e}")
        return redirect('home')
    return redirect('home')

@login_required
def view_cart(request):
    """
    * Handles request to the view-cart path
    * Arguments: no arguments needed it will take all the data from the request made
    * Returns: Render object with a reference to cart.html document
    """
    user = request.user

    cart = get_object_or_404(Cart, user=user)
    products_list = []
    products = cart.product.all()
    for product in products:
        data = {
            'name': product.name,
            'id': product.id,
            'description': product.description,
            'picture': product.picture.url,
            'price': int(product.price),
            }
        products_list.append(data)

    cart_json = json.dumps(products_list)


    return render(request, 'store/cart.html', {'cart': cart, 'cart_json': cart_json})

@login_required
def checkout(request):
    """
    * Handles post requests to the checkout path
       - Creates order for every checked out product
       - Create a payment and add all the orders to the payment and generate a finished payment
    * Arguemts: no arguments it will take the data from the request made
    * Returns: redirect object to the payment_with_id path by linking the payment_id we just created
    """
    if request.method == 'POST':
        selected_orders = request.POST.getlist('items')
        products = []
        user = request.user
        advance = 0
        total_price = 0
        print(selected_orders)
        payment = Payment.objects.create()
        for i in selected_orders:
            product = Product.objects.get(id=i)
            products.append(product)
            color = Color.objects.get(id=request.POST.get(f'{product.id}-color'))
            size = Size.objects.get(id=request.POST.get(f'{product.id}-size'))
            order = Order.objects.create(
                product=product,
                user=request.user,
                color=color,
                size=size,
                cart=request.user.cart)
            order.save()
            payment.orders.add(order)
            payment.save()
        for product in products:
            user.cart.product.remove(product)
        return redirect('payment_with_id', payment_id=payment.id)
        advance += order.payment.advance
        total_price += order.total_price
        print(advance)
        print(advance)
        print(total_price)

        
        return redirect('view_cart')

@login_required
def get_product_data(request, product_id):
    """
    * Handles requests made to the get_product_data path
        - Used for the javascript request that will be made from the frontend
    * Arguments: @product_id - the id of the product we want to get the data of.
    * Return: JsonResponse object(json representation with all the needed info about the product) of the product with the given product_id.
    """
    product = get_object_or_404(Product, id=product_id)
    product_data = {
        'name': product.name,
        'available_colors': [{'name': color.name, 'hex_value': color.hex_value} for color in product.available_colors.all()],
        'sizes': [{'name': size.name, 'short_name': size.short_letter} for size in product.size.all()],
    }
    return JsonResponse(product_data)

@login_required
def my_orders(request):
    """
    * Handles requests made to the my_orders path
        - Checks the users exsistance and get orders related to the user.
    * Arguments: no arguments it will take all that it needs from the request data.
    * Return: Render object referencing the my_orders.html document sending the orders filtered with it.
    """
    if request.user:
        user = request.user
        orders = Order.objects.filter(user=user, cart=None, status='paid')
    return render(request, 'store/my_orders.html', {'orders': orders})

@login_required
def order_details(request):
    if request.method == 'POST':
        generate_qr_code(request.order)


@login_required
def make_payment(request, order_id):
    if request.method == 'POST':
        pass
    order = Order.objects.get(id=order_id)

    code = order.qr_code.url
   
    return render(request, 'store/make_payment.html', {'code': code})


@login_required
def payment(request, order_id):
    print('inside order payment')
    order = Order.objects.get(id=order_id)
    user = request.user
    if request.method == 'POST':
        print(order)
        order.status = 'paid'
        payment = Payment.objects.create()
        payment.status = 'advance paid'
        if order.cart:
            for orders in user.cart.orders.all():
                payment.orders.add(orders)
                if order == orders:
                    print(order)
        order.save()
        return redirect('home')
    payment = order.payment
    print("Payment with order", payment)
    return render(request, 'store/payment.html', {'payment': payment})

@login_required
def payment_with_id(request, payment_id):
    print(payment_id)
    if request.method == 'POST':
        if payment_id:
            payment = Payment.objects.get(id=payment_id)
            payment.status='advance paid'
            for order in payment.orders.all():
                order.save()
        return redirect('home')
    if payment_id:
        payment = Payment.objects.get(id=payment_id)
        print('dict')
        print(payment)
        return render(request, 'store/payment.html', {'payment': payment})