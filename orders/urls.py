from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/', views.create_order, name='create_order'),
    path('history/', views.order_history, name='order_history'),
]
