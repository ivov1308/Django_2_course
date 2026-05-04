"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('users/', include('users.urls')),

    # Подключаем blog/urls.py. Django автоматически использует app_name='blog' оттуда
    path('blog/', include('blog.urls')),
    # Если бы мы подключали его еще раз, мы бы использовали namespace:
    path('company-blog/', include('blog.urls', namespace='company_blog')),

    # Подключаем стандартные URL аутентификации
    # Они будут доступны по префиксу 'accounts/' (например, /accounts/login/, /accounts/logout/)
    path('accounts/', include('django.contrib.auth.urls')),

]
