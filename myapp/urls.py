from django.urls import path, re_path
from . import views

# Этот список urlpatterns будет подключен к главному urls.py проекта
urlpatterns = [
    path('', views.base, name='base'),

    path('hello/', views.simple_view, name='hello_page'), # Новый маршрут
    # path('about/', views.about_page, name='about_page'),   # Новый маршрут
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    # path('', views.index, name='myapp_index'), # Маршрут для корня приложения
    path('details/', views.details, name='myapp_details'),
    path('datetime/', views.current_datetime_view, name='datetime'),
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('static_view/', views.static_view, name='static_view'),
    path('contact_view/', views.contact_view),
    path('contact_success_view/', views.contact_success_view, name='contact_success'),
    path('my-fbv/', views.my_fbv, name='my_fbv_url'),
    # Используем .as_view() для CBV
    path('my-cbv/', views.MyCBV.as_view(), name='my_cbv_url'),


    # Пример с path: только 4 цифры для года
    path('articles//', views.year_archive, name='article_year'),

    # Пример с re_path: 4 цифры для года и 2 цифры для месяца
    # Захватываемые группы передаются как позиционные аргументы в view
    # re_path(r'^articles/(?P[0-9]{4})/(?P[0-9]{2})/$', views.month_archive_regex, name='article_month_regex'),

    # Пример без именованной группы (аргумент будет позиционным)
    re_path(r'^items/([0-9]+)/$', views.item_detail_regex),


    path('set_cookie/', views.set_cookie_view),
    path('read_cookie/', views.read_cookie_view),
    path('delete_cookie/', views.delete_cookie_view),

    path('save_to_session/', views.save_to_session),
    path('read_from_session/', views.read_from_session),
    path('clear_session_data/', views.clear_session_data),

    path('send_test_email/', views.send_test_email),
    path('send_html_email/', views.send_html_email),
    path('send_email_with_attachment/', views.send_email_with_attachment),

]
