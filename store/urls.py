from django.urls import path
from .views import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home')
]