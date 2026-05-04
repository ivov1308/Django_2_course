
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login # Функция для входа пользователя
# from .forms import CustomUserCreationForm # Наша кастомная форма
from django.contrib.auth.forms import UserCreationForm # Или стандартная


class SignUpView(CreateView):
    # form_class = CustomUserCreationForm
    form_class = UserCreationForm # Используем стандартную форму
    template_name = 'registration/signup.html' # Шаблон для формы регистрации
    success_url = reverse_lazy('users:signup_success') # URL для редиректа после успеха

    def form_valid(self, form):
        # Стандартное поведение CreateView сохраняет форму (form.save())
        # и возвращает HttpResponseRedirect на success_url.
        # Мы хотим сначала сохранить пользователя, а потом залогинить его.
        response = super().form_valid(form)

        # self.object содержит созданный объект пользователя
        user = self.object

        # Выполняем вход пользователя
        login(self.request, user)

        # Возвращаем редирект, который сформировал super().form_valid()
        return response


# Можно добавить простое представление для страницы успеха
def signup_success_view(request):
    return render(request, 'registration/signup_success.html')
