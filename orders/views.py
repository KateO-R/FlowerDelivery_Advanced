from django.shortcuts import render, redirect
from .models import Product, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order
from .forms import OrderForm


def home(request):
    products = Product.objects.all()
    return render(request, 'orders/home.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'orders/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'orders/profile.html')

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'orders/product_list.html', {'products': products})


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)  # Получаем товары в корзине текущего пользователя
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # Общая сумма

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            # Сохраняем товары корзины как часть заказа
            for item in cart_items:
                order.products.add(item.product, through_defaults={'quantity': item.quantity})
            cart_items.delete()  # Очищаем корзину
            return render(request, 'orders/order_success.html', {'message': "Thank you for your order. You can track its status in your profile or Telegram bot."})
    else:
        form = OrderForm()

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

