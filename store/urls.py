from django.urls import path
from .views import views, order_views, catagory_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('order/<int:product_id>/', order_views.order, name='order'),
    path('order/<int:product_id>/<str:cart>', order_views.order, name='order_for_cart'),
    path('add-to-cart/<int:product_id>/', order_views.add_to_cart, name="add_to_cart"),
    path('view-cart/', order_views.view_cart, name="view_cart"),
    path('checkout/<int:order_id>', order_views.checkout, name="checkout"),
    path('filter_by_category/<int:category_id>', catagory_views.filter_product_by_category, name='filter_product_by_category'),
    path('get_product_data/<int:product_id>/', order_views.get_product_data, name='get_product_data'),
    path('my_orders/', order_views.my_orders, name='my_orders'),
    path('order-details/', order_views.order_details, name='order-details'),
    path('make-payment/<int:order_id>', order_views.make_payment, name='make_payment'),
    path('payment/<int:order_id>', order_views.payment, name='payment'),
]