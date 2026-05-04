
from django import forms
from .models import Post # Импортируем нашу модель

class PostForm(forms.ModelForm):
    class Meta:
        model = Post # Указываем модель, на основе которой создается форма
        # Включаем только нужные поля в форму
        fields = ('title', 'content', 'author')
        # Или можно было бы исключить ненужные:
        # exclude = ('created_date', 'published_date')

        # Можно также настроить виджеты или метки прямо здесь
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'author': forms.HiddenInput(), # Например, если автор будет устанавливаться автоматически
        }
        labels = {
            'title': 'Заголовок Поста',
            'content': 'Содержимое',
        }
        help_texts = {
            'title': 'Придумайте яркий заголовок!',
        }
        # error_messages = { ... }
