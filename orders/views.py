from django.shortcuts import render, redirect
from .models import Product, Order, OrderProduct
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order
from .forms import OrderForm, SignUpForm


def home(request):
    products = Product.objects.all()
    return render(request, 'orders/home.html', {'products': products})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним пользователя после регистрации
            return redirect("profile")  # Перенаправляем в профиль
    else:
        form = SignUpForm()
    return render(request, "orders/signup.html", {"form": form})

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/profile.html', {'orders': orders})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'orders/product_list.html', {'products': products})


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)  # Получаем товары в корзине текущего пользователя
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # Общая сумма
    is_empty = cart_items.count() == 0  # Проверяем, пустая ли корзина
    message = None

    # Интервалы доставки
    delivery_times = ['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00']

    if request.method == 'POST' and not is_empty:  # Обработка формы заказа, если корзина не пуста
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.delivery_date = form.cleaned_data['delivery_date']
            order.time = form.cleaned_data['time']
            order.address = form.cleaned_data['address']
            order.recipient = form.cleaned_data['recipient']
            order.total_price = total_price
            order.save()

            # Добавляем товары в заказ
            for item in cart_items:
                OrderProduct.objects.create(order=order, product=item.product, quantity=item.quantity)
                item.total_price = item.product.price * item.quantity

            print("Cart items before delete:", cart_items)  # Отладка перед очисткой корзины
            cart_items.delete()  # Очищаем корзину после оформления заказа
            print("Cart items after delete:", CartItem.objects.filter(user=request.user))  # Проверяем очистку корзины

            message = "Thank you for your order. You can track its status in your profile or Telegram bot."
            form = OrderForm()  # Сброс формы после успешного заказа
        else:
            # Если форма невалидна, логируем ошибки для отладки
            print(form.errors)
    else:
        form = OrderForm()

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'is_empty': is_empty,
        'form': form,
        'delivery_times': delivery_times,  # Добавляем интервалы доставки в шаблон
        'message': message,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем товар или возвращаем 404
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1  # Увеличиваем количество, если товар уже в корзине
        cart_item.save()
    return redirect('cart')  # Перенаправляем пользователя на страницу корзины

@login_required
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'decrease' and cart_item.quantity == 1:
        cart_item.delete()
        return redirect('cart')  # Перенаправляем обратно в корзину, если товар удален

    cart_item.save()
    return redirect('cart')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def repeat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Получаем корзину из сессии
    cart = request.session.get('cart', {})

    for order_product in order.orderproduct_set.all():
        product_id = str(order_product.product.id)

        # Если товар уже есть в корзине — увеличиваем количество
        if product_id in cart:
            cart[product_id]['quantity'] += order_product.quantity
        else:
            cart[product_id] = {
                'name': order_product.product.name,
                'price': float(order_product.product.price),
                'quantity': order_product.quantity,
                'image': order_product.product.image.url
            }

    # Сохраняем обновленную корзину в сессии
    request.session['cart'] = cart
    return redirect('cart')