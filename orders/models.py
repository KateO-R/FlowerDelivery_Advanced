from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с товаром
    quantity = models.PositiveIntegerField(default=1)  # Количество товара в корзине

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) for {self.user.username}"

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Order #{self.order.id})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct', related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=502, default="No time chosen")
    address = models.CharField(max_length=255, default="No address provided")
    recipient = models.CharField(max_length=100, default="No recipient provided")

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.orderproduct_set.all())
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True)  # Telegram ID как число

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"