from django.test import TestCase
from orders.models import CustomUser, Product, Order, CartItem

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            phone_number="+79001234567",
            address="Test Street 123",
            password="12345"
        )
        self.order = Order.objects.create(user=self.user, status="pending")

    def test_order_creation(self):
        """Тест создания заказа"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, "pending")


class CartViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            phone_number="+79001234567",
            address="Test Street 123",
            password="12345"
        )
        self.product = Product.objects.create(name="Test Bouquet", price=100.0)

    def test_add_to_cart(self):
        """Тест добавления товара в корзину"""
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        cart_items = CartItem.objects.filter(user=self.user)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.first().product.name, "Test Bouquet")
