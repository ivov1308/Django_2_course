from django.urls import path
from .views import (SignUpView,
                    signup_success_view
                    )

app_name = 'users' # Определяем пространство имен для этого приложения

# Этот список urlpatterns будет подключен к главному urls.py проекта
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_success/', signup_success_view, name='signup_success'),

]
