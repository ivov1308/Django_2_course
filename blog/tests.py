
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post # Пример модели

class BlogViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Метод для создания данных, общих для всех тестов в классе
        # Вызывается один раз перед запуском тестов класса

        user_1 = User()
        user_1.username = "user1"
        user_1.password = "user1_pass"
        user_1.save()

        user_2 = User()
        user_2.username = "user2"
        user_2.password = "user2_pass"
        user_2.save()

        Post.objects.create(
            title="Test Title 1",
            content="Большое текстовое поле без ограничения",
            author=user_1
        )
        Post.objects.create(
            title="Test Title 2",
            content="Большое текстовое поле без ограничения",
            author=user_2
        )
        print("setUpTestData: Созданы тестовые данные")

    def setUp(self):
        # Метод вызывается ПЕРЕД каждым тестовым методом
        # Создаем экземпляр тестового клиента
        self.client = Client()
        print(f"setUp: Запуск теста {self._testMethodName}")

    def tearDown(self):
        # Метод вызывается ПОСЛЕ каждого тестового метода
        # Используется редко, т.к. TestCase откатывает транзакции
        print(f"tearDown: Завершение теста {self._testMethodName}")

    def test_list_view_status_code(self):
        """Проверяет, что страница списка доступна (статус 200)."""
        url = reverse('blog:post_list') # Получаем URL по имени
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Проверяет, что используется правильный шаблон."""
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_list_view_contains_data(self):
        """Проверяет, что на странице списка отображаются данные."""
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertContains(response, "Test Title 1")
        self.assertContains(response, "Test Title 2")

    def test_detail_view_status_code(self):
        """Проверяет доступность детальной страницы."""
        item = Post.objects.get(title="Test Title 1")
        url = reverse('blog:post_detail', kwargs={'pk': item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Другие тесты: для POST-запросов, форм, логики моделей и т.д.
