from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.product_list, name='product_list'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('history/', views.order_history, name='order_history'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
