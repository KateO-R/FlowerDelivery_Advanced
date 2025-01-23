from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_list/', views.product_list, name='product_list'),  # Исправленный путь
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Новый маршрут
    path('cart/update/<int:cart_item_id>/<str:action>/', views.update_cart, name='update_cart'),  # Новый маршрут
    path('history/', views.order_history, name='order_history'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
