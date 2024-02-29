### API для вывода информации о продуктах, уроках и статистике просмотра уроков пользователями (Django Rest Framework + Django).

### Установка
Клонируйте репозиторий https://github.com/NadinKon/EduBridge.git <br>

Установите зависимости: <br>
pip install -r requirements.txt

**Примените миграции** <br>
python manage.py migrate 

**Создайте админа** <br>
python manage.py createsuperuser

**Загрузите начальные данные в БД** <br>
python manage.py loaddata products.json accesses.json lessons.json groups.json

### Использование
Запустить локально сервер разработки Django: <br>
python manage.py runserver

Тестировать можно по адресу: <br>
http://127.0.0.1:8000/admin - админ панель <br> 
http://127.0.0.1:8000/products/ - список продуктов <br>
http://127.0.0.1:8000/products/1/lessons/ - заменить 1 на ID интересующего продукта <br>
http://127.0.0.1:8000/product-stats/ - проверить статистику по всем продуктам
