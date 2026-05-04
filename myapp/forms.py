from django.forms import (Form,
                          CharField,
                          EmailField,
                          Textarea,
                          BooleanField,)

class ContactForm(Form):
    # Поля формы
    name = CharField(
        max_length=100,
        label='Ваше имя', # Метка для поля (используется при рендеринге)
        required=True,   # Поле обязательно для заполнения (по умолчанию True)
        help_text='Введите полное имя' # Текст подсказки
    )
    email = EmailField(
        label='Ваш Email',
        required=True
    )
    subject = CharField(
        max_length=200,
        label='Тема сообщения',
        required=True
    )
    message = CharField(
        widget=Textarea, # Используем виджет Textarea для многострочного ввода
        label='Сообщение',
        required=True
    )
    cc_myself = BooleanField(
        required=False, # Поле не обязательно
        label='Отправить копию себе'
    )

    # Можно добавлять свои методы валидации (об этом позже)


class MyForm(Form):
    pass


