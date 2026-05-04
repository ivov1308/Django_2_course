
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=150, required=False, label="Фамилия")

    class Meta(UserCreationForm.Meta):
        model = User # Используем стандартную модель User
        # Включаем стандартные поля UserCreationForm + наши новые поля
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

