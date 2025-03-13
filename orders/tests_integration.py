from django.test import TestCase, Client
from django.urls import reverse
from orders.models import CustomUser, Product, CartItem, Order, OrderProduct

class IntegrationTest(TestCase):
    def setUp(self):
        """Настройка тестового пользователя и товаров"""
        self.client = Client()  # Клиент для имитации запросов
        self.user = CustomUser.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            phone_number="+79001234567",
            address="Test Street 123",
            password="testpassword"
        )
        self.client.login(username="testuser", password="12345")  # Логинимся

        self.product = Product.objects.create(name="Test Bouquet", price=100.0)

    def test_cart_to_order_integration(self):
        """Тест: добавление в корзину -> оформление заказа -> проверка заказа"""
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

        # Логиним пользователя перед тестом оформления заказа
        print(f"Logging in as: {self.user.email}, password: testpassword")
        login_successful = self.client.login(username=self.user.email, password="testpassword")
        print(f"Login successful: {login_successful}")
        assert login_successful, "❌ Не удалось выполнить вход! Проверь данные пользователя."

        self.product = Product.objects.create(name="Test Bouquet", price=100.0)

        # Оформляем заказ
        response = self.client.post(reverse("cart"), data={
            "delivery_date": "2025-03-20",
            "time": "12:00-15:00",
            "address": "Test Address",
            "recipient": "John Doe"
        }, follow=True)

        # 🔍 Отладка: проверяем статус ответа и ошибки формы
        print("Response status:", response.status_code)
        print("Response URL:", response.request["PATH_INFO"])  # Покажет, на какой странице оказался пользователь
        print("Form errors:", response.context["form"].errors if response.context and "form" in response.context else "No form context")

        # Проверяем, что заказ создан
        orders = Order.objects.filter(user=self.user)
        print("Existing orders in test DB:", list(Order.objects.values()))
        self.assertEqual(orders.count(), 1)

    def test_order_status_update(self):
        """Тест: изменение статуса заказа"""
        order = Order.objects.create(user=self.user, status="pending")

        # Меняем статус заказа
        order.status = "delivered"
        order.save()

        # Проверяем, что статус обновился
        updated_order = Order.objects.get(id=order.id)
        self.assertEqual(updated_order.status, "delivered")