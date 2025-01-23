from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'products',
            'status',
            'delivery_date',
            'delivery_time',
            'delivery_address',
            'recipient',
        ]