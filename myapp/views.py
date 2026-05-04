from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
import datetime
from .forms import ContactForm, MyForm
from django.views import View
from django.conf import settings # Для доступа к DEFAULT_FROM_EMAIL

# Create your views here.


def simple_view(request):
    # request - это объект HttpRequest
    # Здесь может быть ваша логика
    text_content = "Привет, мир! Это мое первое представление Django."
    # Мы должны вернуть объект HttpResponse
    return HttpResponse(text_content)

def about_page(request):
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>О нас</title>
</head>
<body>
    <h1>Страница 'О нас'</h1>
    <p>Это простая страница, созданная с помощью Django view.</p>
</body>
</html>
"""
    return HttpResponse(html_content)


def item_detail(request, item_id):
    pass

def index(request):
    return render(request, 'myapp/index.html')

def details(request):
    pass


def current_datetime_view(request):
    now = datetime.datetime.now()
    user_agent = request.headers.get('User-Agent', 'не определен') # Получаем User-Agent из запроса

    # Создаем словарь контекста
    context = {
        'current_time': now,
        'browser_info': user_agent,
        'user_is_active': True,
        'item_list': ['Яблоко', 'Банан', 'Апельсин']
    }

    # Отрисовываем шаблон 'myapp/datetime_page.html' с этим контекстом
    return render(request, 'myapp/datetime_page.html', context)


def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'myapp/about_page.html')


def static_view(request):
    return render(request, 'myapp/static_page.html')


def contact_view(request):
    if request.method == 'POST':
        # 1. Создаем экземпляр формы и заполняем его данными из запроса (request.POST)
        form = ContactForm(request.POST)

        # 2. Проверяем валидность данных
        if form.is_valid():
            # 3. Данные валидны. Обрабатываем их.
            # Атрибут form.cleaned_data содержит очищенные и проверенные данные
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            cc_myself = form.cleaned_data['cc_myself']

            # Пример действия: отправка email
            recipients = ['ilya.klimenko.01@list.ru']
            if cc_myself:
                recipients.append(email)

            try:
                send_mail(
                    f'Сообщение с сайта: {subject}', # Тема письма
                    f'От: {name} <{email}>\n\n{message}', # Тело письма
                    'noreply@example.com', # Адрес отправителя (должен быть настроен в settings.py)
                    recipients, # Список получателей
                    fail_silently=False, # Если True, не будет выбрасывать исключений при ошибке отправки
                )
                # 4. Перенаправляем пользователя после успешной обработки
                # Это стандартная практика после POST-запроса (Post/Redirect/Get pattern)
                return redirect('contact_success') # Перенаправляем на URL с именем 'contact_success'
                # Или: return HttpResponseRedirect('/contact/success/')
            except Exception as e:
                # Здесь можно добавить логирование ошибки
                # и, возможно, показать пользователю сообщение об ошибке отправки
                form.add_error(None, f"Ошибка отправки письма: {e}") # Добавляем общую ошибку к форме

        # Если form.is_valid() == False, управление перейдет сюда автоматически
        # или если была ошибка отправки и мы не сделали редирект

    else: # Если это GET-запрос (или любой другой метод)
        # Создаем пустую форму для отображения
        form = ContactForm()

    # Отображаем шаблон:
    # - Если GET: с пустой формой
    # - Если POST и невалидно: с заполненной формой и ошибками
    # - Если POST и ошибка отправки: с заполненной формой и общей ошибкой
    context = {
        'form': form,
        'page_title': 'Свяжитесь с нами'
    }
    return render(request, 'myapp/contact_page.html', context)


# Представление для страницы успешной отправки
def contact_success_view(request):
     return render(request, 'myapp/contact_success.html')


# --- Function-Based View ---
def my_fbv(request):
    if request.method == 'GET':
        # Логика для GET
        form = MyForm()
        return render(request, 'myapp/template.html', {'form': form})
    elif request.method == 'POST':
        # Логика для POST
        form = MyForm(request.POST)
        if form.is_valid():
            # Обработка валидных данных
            return HttpResponse("Form submitted successfully!")
        else:
            # Показать форму с ошибками
            return render(request, 'myapp/template.html', {'form': form})
    else:
        # Обработка других методов (не обязательно)
        return HttpResponse(status=405) # Method Not Allowed

# --- Class-Based View (аналог) ---
class MyCBV(View):
    form_class = MyForm
    template_name = 'myapp/template.html'

    def get(self, request, *args, **kwargs):
        # Логика для GET-запроса
        form = self.form_class()
        print(f"ARGS in GET: {args}")     # Дополнительные позиционные аргументы из URL
        print(f"KWARGS in GET: {kwargs}") # Дополнительные именованные аргументы из URL (например, pk)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Логика для POST-запроса
        form = self.form_class(request.POST)
        if form.is_valid():
            # Обработка валидных данных
            # Например: form.save() для ModelForm
            return HttpResponse("Form submitted successfully via CBV!")
        else:
            # Показать форму с ошибками
            return render(request, self.template_name, {'form': form})

    # Можно определить методы для других HTTP-глаголов: put, delete, head, options, trace
    # def put(self, request, *args, **kwargs): ...


# Представление для re_path с именованными группами
def year_archive(request, year, month): ...

# Представление для re_path с именованными группами
def month_archive_regex(request, year, month): ...

# Представление для re_path без именованных групп
def item_detail_regex(request, item_id): ...


# Установка cookie в представлении
def set_cookie_view(request):
    response = HttpResponse("Cookie установлено!")
    response.set_cookie(
        'my_preference',
        'dark_theme',
        max_age=3600 * 24 * 7, # Время жизни - 1 неделя в секундах
        httponly=True,
        samesite='Lax'
     )
    return response

# Чтение cookie в представлении
def read_cookie_view(request):
    preference = request.COOKIES.get('my_preference', 'light_theme') # Получаем значение, или 'light_theme' по умолчанию
    return HttpResponse(f"Ваша тема: {preference}")

# Удаление cookie
def delete_cookie_view(request):
    response = HttpResponse("Cookie удалено!")
    response.delete_cookie('my_preference')
    return response


# Запись данных в сессию
def save_to_session(request):
    request.session['favorite_color'] = 'blue'
    request.session['view_count'] = request.session.get('view_count', 0) + 1
    # Сессия автоматически сохраняется при модификации
    return HttpResponse(f"Данные сохранены. Счетчик просмотров: {request.session['view_count']}")

# Чтение данных из сессии
def read_from_session(request):
    color = request.session.get('favorite_color', 'неизвестен') # .get() с дефолтом безопаснее
    count = request.session.get('view_count', 0)
    return HttpResponse(f"Любимый цвет: {color}. Счетчик: {count}")

# Удаление данных из сессии
def clear_session_data(request):
    # Удалить конкретный ключ
    if 'favorite_color' in request.session:
        del request.session['favorite_color']

    # Очистить все данные сессии (но не удалить саму сессию и cookie)
    request.session.flush() # Это удалит и данные, и cookie сессии (пользователь "разлогинится")

    return HttpResponse("Данные сессии изменены.")


def send_test_email(request):
    subject = 'Тестовое письмо от Django'
    message = 'Привет! Это простое тестовое сообщение.'
    from_email = settings.DEFAULT_FROM_EMAIL # Или указать явно
    recipient_list = ['ilya.klimenko.01@list.ru']

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Письмо успешно отправлено (или выведено в консоль).")
    except Exception as e:
        # В реальном приложении здесь должно быть логирование
        return HttpResponse(f"Ошибка отправки письма: {e}", status=500)


def send_html_email(request):
    subject = 'HTML Письмо от Django'
    text_content = 'Это текстовая версия письма для клиентов без поддержки HTML.'
    html_content = '<h1>Привет!</h1>\n<p>Это HTML версия письма.<p>'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['ilya.klimenko.01@list.ru']
    try:
        send_mail(subject, text_content, from_email, recipient_list, html_message=html_content)
        return HttpResponse("HTML Письмо отправлено.")
    except Exception as e:
        return HttpResponse(f"Ошибка отправки HTML письма: {e}", status=500)


def send_email_with_attachment(request):
    subject = 'Письмо с вложением'
    body = 'Пожалуйста, найдите вложение.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = ['ilya.klimenko.01@list.ru']
    cc = ['ivan13air@mail.ru']
    bcc = ['ilya.klimenko.01@list.ru']

# Поле «To:» содержит адрес(а) основного полячателя (получателей) сообщения.
# Поле «Cc:» (от «Carbon Copy» - копия по аналогии с печатью под копирку на пишущей машинке) содержит адреса
# других лиц, которым направляется это сообщение, хотя содержимое сообщения может быть не адресовано им
# напрямую.
# Поле «Bcc:» (от «Blind Carbon Copy» - «слепая копия» по аналогии с последним экземпляром при печати под копирку)
# содержит адреса получателей, которые не будут показаны другим получателям этого сообщения.

    email = EmailMessage(
        subject,
        body,
        from_email,
        to,
        bcc,
        cc=cc,
        # headers={'Reply-To': 'another@example.com'} # Дополнительные заголовки
    )

    # Добавление вложения из файла
    try:
        from myproject.settings import BASE_DIR
        with open(BASE_DIR / 'resources/SGC_info.pdf', 'rb') as f:
            email.attach('SGC_info.pdf', f.read(), 'application/pdf')
    except FileNotFoundError:
       pass # Обработка ошибки

    # Добавление вложения из строки
    # email.attach('signature.txt', 'С уважением,...', 'text/plain')

    try:
        email.send(fail_silently=False)
        return HttpResponse("Письмо с вложением отправлено.")
    except Exception as e:
        return HttpResponse(f"Ошибка отправки письма с вложением: {e}", status=500)
