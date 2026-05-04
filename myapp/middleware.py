import time

class SimpleTimingMiddleware:
    def __init__(self, get_response):
        # Одноразовая настройка и инициализация при старте сервера
        self.get_response = get_response

    def __call__(self, request):
        # Код, выполняемый для КАЖДОГО запроса ПЕРЕД
        # вызовом представления (и последующих middleware)
        start_time = time.time()

        # Вызываем следующий middleware или представление
        response = self.get_response(request)

        # Код, выполняемый для КАЖДОГО ответа ПОСЛЕ
        # выполнения представления
        duration = time.time() - start_time
        print(f"Запрос к {request.path} занял {duration:.4f} секунд")
        print(f'{response=}')
        
        # Можно модифицировать response здесь, например, добавить заголовок
        response['X-Processing-Time-Seconds'] = f"{duration:.4f}"

        return response
