from datetime import datetime, timedelta, timezone
from django.contrib import admin
from .models import Post, Category, Comment


# Класс для настройки отображения модели Post в админке
class PostAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в виде колонок на странице списка постов
    list_display = ('title', 'author', 'created_date', 'published_date', 'was_published_recently')

    # Поля, по которым можно будет фильтровать список справа
    list_filter = ('published_date', 'created_date', 'author')

    # Поля, по которым будет работать поиск
    search_fields = ('title', 'content')

    # Порядок полей в форме редактирования/создания
    # fields = ('author', 'title', 'content', 'published_date') # Простой вариант

    # Более сложная группировка полей:
    fieldsets = (
        (None, { # Группа без заголовка
            'fields': ('author', 'title', 'content')
        }),
        ('Даты', { # Группа с заголовком 'Даты'
            'fields': ('created_date', 'published_date'),
            'classes': ('collapse',) # Сделать группу сворачиваемой
        }),
    )
    # Добавляем вычисляемое поле (метод из модели Post)
    readonly_fields = ('created_date',) # Поля только для чтения

    # Метод для вычисляемой колонки в list_display
    @admin.display(boolean=True, description='Опубликовано недавно?')
    def was_published_recently(self, obj):
        # Пример использования метода из модели (если он есть)
        # return obj.was_published_recently()
        # Или своя логика прямо здесь
        now = datetime.now(timezone.utc)
        return now - timedelta(days=1) <= obj.published_date if obj.published_date else False


# Класс для настройки Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    search_fields = ('post',)
    prepopulated_fields = {'category': ('post',)} # Автозаполнение slug на основе name


# Регистрируем модели С указанием их классов настроек
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

# Можно использовать декоратор @admin.register() как альтернативу admin.site.register()
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_date', 'text')
    list_filter = ('author_name', 'created_date')
    search_fields = ('author_name', 'text')
