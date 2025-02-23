from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order


class OrderForm(forms.ModelForm):
    TIME_CHOICES = [
        ('09:00-12:00', '09:00-12:00'),
        ('12:00-15:00', '12:00-15:00'),
        ('15:00-18:00', '15:00-18:00'),
        ('18:00-21:00', '18:00-21:00'),
    ]

    time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)

    class Meta:
        model = Order
        fields = [
            'delivery_date',
            'time',
            'address',
            'recipient',
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text="Enter your phone number")
    address = forms.CharField(max_length=255, required=True, help_text="Enter your address")
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'address', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.address = self.cleaned_data["address"]
        user.set_password(self.cleaned_data["password1"])  # Устанавливаем пароль
        if commit:
            user.save()
        return user