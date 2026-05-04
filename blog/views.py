
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Post # Импортируем нашу модель Post
from .forms import PostForm
# from django.contrib.auth.decorators import login_required # Обычно нужно ограничить доступ

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # Для "ленивого" определения URL
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView
)

def blog(request):
    return render(request, 'blog/blog.html')


# @login_required
def post_list_view(request):
    # 1. Получаем данные: все опубликованные посты, отсортированные по дате (новые первыми)
    published_posts = Post.objects.filter().order_by('-published_date')

    # 2. Формируем контекст
    context = {
        'post_list': published_posts, # Передаем QuerySet в шаблон под именем 'post_list'
        'page_title': 'Наш Блог',
    }

    # 3. Рендерим шаблон
    return render(request, 'blog/post_list.html', context)

# @login_required
def post_detail_view(request, pk): # Принимаем pk (primary key) из URL
    # 1. Получаем данные: один конкретный пост по его ID
    try:
        post = Post.objects.get(pk=pk) # pk - это сокращение для primary key (обычно id)
    except Post.DoesNotExist:
        # В реальном приложении здесь лучше вернуть 404 Not Found
        from django.http import Http404
        raise Http404("Пост не найден")
        # Для простоты пока вернем пустой контекст или редирект
        return render(request, 'blog/post_not_found.html') # Нужен такой шаблон

    # 2. Формируем контекст
    context = {
        'post': post, # Передаем один объект поста
    }

    # 3. Рендерим шаблон
    return render(request, 'blog/post_detail.html', context)


# @login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Если нужно что-то сделать до сохранения (например, установить автора)
            new_post = form.save(commit=False)
            new_post.author = request.user # Устанавливаем текущего пользователя как автора
            new_post.save() # Сохраняем объект в БД
            # form.save_m2m() # Если бы были M2M поля

            # Или если все поля есть в форме и автора установили через HiddenInput или Meta.widgets
            # post = form.save() # commit=True по умолчанию

            return redirect('blog:post_detail', pk=new_post.pk) # Перенаправляем на просмотр созданного поста
    else:
        # form = PostForm()
        # Можно установить начальные значения, если нужно
        form = PostForm(initial={'author': request.user})


    return render(request, 'blog/post_new.html', {'form': form, 'page_title': 'Создать пост'})


# @login_required
def edit_post_view(request, pk):
    post_instance = get_object_or_404(Post, pk=pk) # Получаем пост для редактирования

    # Проверка прав доступа (например, редактировать может только автор)
    # if post_instance.author != request.user:
    #     return Http404  # redirect('some_error_page')

    if request.method == 'POST':
        # Передаем instance в конструктор формы для обновления
        form = PostForm(request.POST, instance=post_instance)

        if form.is_valid():
            form.save() # Обновляем существующий объект
            return redirect('blog:post_detail', pk=post_instance.pk)
    else:
        # Передаем instance для предзаполнения формы текущими данными поста
        form = PostForm(instance=post_instance)

    context = {
        'post': post_instance,
        'form': form,
        'page_title': 'Редактировать пост'
    }

    return render(request, 'blog/post_edit.html', context)


class PostListView(ListView, LoginRequiredMixin, TemplateView):
    model = Post  # Указываем модель, объекты которой нужно вывести
    template_name = 'blog/post_list.html'  # Указываем шаблон для отображения
    context_object_name = 'post_list'  # Имя переменной со списком объектов в шаблоне (по умолчанию object_list)
    queryset = Post.objects.filter().order_by('-published_date') # Можно указать свой QuerySet
    paginate_by = 10 # Включаем пагинацию (по 10 постов на страницу)
    object_list = queryset

class PostDetailView(DetailView, UserPassesTestMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' # Имя переменной с объектом поста в шаблоне (по умолчанию object)
    # pk_url_kwarg = 'post_id' # Если в URL параметр называется не 'pk' или 'slug'

    def test_func(self):
        # Разрешить доступ только персоналу (is_staff)
        return self.request.user.is_staff


class PostCreateView(CreateView, PermissionRequiredMixin):
    model = Post
    # form_class = PostForm # Если используем свою форму
    fields = ['title', 'content', 'author'] # Или указываем поля для авто-генерации ModelForm
    template_name = 'blog/post_new.html' # Шаблон с формой
    # success_url = reverse_lazy('post_list') # URL для редиректа после успешного создания

    permission_required = 'blog.add_post' # noqa #Требуемое право
    raise_exception = True # Выбросить исключение при нехватке прав

    # Можно переопределить form_valid для добавления логики перед сохранением
    def form_valid(self, form):
        # form.instance.author = self.request.user # Пример: Установить автора
        return super().form_valid(form)

    # Можно переопределить get_success_url для динамического URL
    def get_success_url(self):
        # return reverse('post_detail', kwargs={'pk': self.object.pk}) # Редирект на созданный пост
        return reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content'] # Поля, доступные для редактирования
    template_name = 'blog/post_edit.html' # Тот же шаблон, что и для создания
    success_url = reverse_lazy('blog:post_list')
    # context_object_name = 'post' # По умолчанию 'object'

    # Можно добавить проверку прав доступа, переопределив dispatch или get_object
    # def get_queryset(self):
    #    qs = super().get_queryset()
    #    return qs.filter(author=self.request.user) # Разрешить редактировать только свои посты


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html' # Шаблон с подтверждением удаления
    success_url = reverse_lazy('blog:post_list') # URL для редиректа после удаления
    # context_object_name = 'post' # По умолчанию 'object'
