from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'delivery_date',
            'time',
            'address',
            'recipient',
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),  # Включение HTML5 календаря
        }