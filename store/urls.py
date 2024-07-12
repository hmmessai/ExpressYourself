from django.urls import path
from .views import views, order_views

urlpatterns = [
    path('', views.index, name='index'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('order/<int:product_id>/<int:user_id>/', order_views.order, name='order'),
    path('add-to-cart/<int:product_id>/', order_views.add_to_cart, name="add_to_cart"),
    path('view-cart/', order_views.view_cart, name="view_cart"),
    path('checkout/', order_views.checkout, name="checkout"),
]