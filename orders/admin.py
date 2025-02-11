from django.contrib import admin
from .models import Product, Order, Profile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'order_date')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'telegram_id')  # Добавили номер телефона
    search_fields = ('user__username', 'phone_number')  # Поиск по имени и номеру
    