from django.urls import path
from users import views

urlpatterns = [
    path('view_profile/', views.ViewProfile.as_view(), name='view_profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogOutView.as_view(), name='logout'),
]