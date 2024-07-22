from django.urls import path
from .views import views, order_views, catagory_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('order/<int:product_id>/', order_views.order, name='order'),
    path('add-to-cart/<int:product_id>/', order_views.add_to_cart, name="add_to_cart"),
    path('view-cart/', order_views.view_cart, name="view_cart"),
    path('checkout/', order_views.checkout, name="checkout"),
    path('filter_by_category/<int:category_id>', catagory_views.filter_product_by_category, name='filter_product_by_category'),
    path('get_product_data/<int:product_id>/', order_views.get_product_data, name='get_product_data'),
]