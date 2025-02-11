from django import forms
from django.contrib.auth.models import User
from .models import Order, Profile


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
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),  # Включение HTML5 календаря
        }

# Форма регистрации с добавлением номера телефона
class SignUpForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text="Enter your phone number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Устанавливаем пароль
        if commit:
            user.save()
            Profile.objects.create(user=user, phone_number=self.cleaned_data["phone_number"])  # Создаем профиль
        return user