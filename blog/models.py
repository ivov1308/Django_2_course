from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE
)
from django.utils import timezone # Для установки времени по умолчанию
from django.contrib.auth.models import User # Для связи с пользователями (авторами)


class Post(Model):
    # Поля модели (соответствуют столбцам таблицы blog_post)
    title = CharField(max_length=200) # Текстовое поле с ограничением длины
    content = TextField()             # Большое текстовое поле без ограничения (в большинстве БД)
    created_date = DateTimeField(default=timezone.now) # Дата и время с значением по умолчанию
    published_date = DateTimeField(blank=True, null=True) # Дата и время, может быть пустым
    author = ForeignKey(User, on_delete=CASCADE) # Ссылка на другую модель (User)

    # Методы модели (не создают столбцов в БД)
    def publish(self):
        self.published_date = timezone.now()
        self.save() # Сохраняет изменения объекта в БД

    def __str__(self):
        # Возвращает строковое представление объекта (удобно в админке и shell)
        return self.title


# Можно определить другие модели...
class Comment(Model):
   post = ForeignKey(Post, related_name='comments', on_delete=CASCADE)
   author_name = CharField(max_length=100)
   text = TextField()
   created_date = DateTimeField(default=timezone.now)

   def __str__(self):
       return f'Comment by {self.author_name} on {self.post}'


class Category(Model):
    post = ForeignKey(Post, related_name='category', on_delete=CASCADE)
    category = CharField(max_length=100)
    description = TextField(blank=True, null=True)

    def __str__(self):
       return f'The category of post {self.post} is {self.category}'
