from django.urls import path
from .views import views

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name="signup")
]