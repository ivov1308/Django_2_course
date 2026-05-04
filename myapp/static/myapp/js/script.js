document.addEventListener('DOMContentLoaded', function() {
// Ждём, пока вся HTML-страница полностью загрузится

    document.getElementById('myButton').addEventListener('click', function() {
    // Находим кнопку по id "myButton"

        alert('Привет из внешнего файла! \n /static/js/script.js');
        // При клике показываем всплывающее окно с сообщением
    });

});
// Закрываем обе функции: сначала ту, что реагирует на клик, затем ту, что ждёт загрузки страницы.