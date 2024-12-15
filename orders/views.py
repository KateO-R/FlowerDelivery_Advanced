from django.shortcuts import render, redirect
from .models import Product, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

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
def product_list(request):
    products = Product.objects.all()
    return render(request, 'orders/product_list.html', {'products': products})


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()
            return redirect('order_history')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})
