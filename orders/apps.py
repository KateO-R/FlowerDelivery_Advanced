from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        import bot.tasks
        print("✅ orders.apps: Подключаем сигналы...")
        print("✅ orders.apps: tasks.py загружен!")  # <-- Для отладки