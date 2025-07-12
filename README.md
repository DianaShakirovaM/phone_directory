# Телефонный справочник организации
### Корпоративный телефонный справочник - это веб-приложение для управления контактной информацией сотрудников организации. Система предоставляет удобный интерфейс для поиска, добавления, редактирования и удаления контактов, а также поддерживает импорт/экспорт данных.
---
# Основные функции
- 📌 Просмотр списка сотрудников с группировкой по подразделениям
- 🔍 Поиск по ФИО, должности, телефону и другим параметрам
- ➕ Добавление новых контактов через интуитивно понятную форму
- ✏️ Редактирование существующих записей
- 🗑️ Удаление контактов с подтверждением операции
- 📥 Импорт данных из CSV-файлов
- 📤 Экспорт данных в различных форматах (CSV)
---
# Технологии
Backend:
- Python 3.3+
- Django 3.2+

Frontend:
- HTML5, CSS3
- Bootstrap 5
- JavaScript (ES6+)
--- 
# Установка и запуск
Клонировать репозиторий:
```bash
git clone https://github.com/DianaShakirovaM/phone_directory.git
cd phone-directory
```
Создать и активировать виртуальное окружение:
```bash
  python -m venv venv
  source venv/bin/activate  # Linux/MacOS
  venv\Scripts\activate  # Windows
```
Установить зависимости:
```bash
pip install -r requirements.txt
```
Настроить базу данных в файле settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'phone_directory',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Выполнить миграции:
```bash
python manage.py migrate
```
Запустить сервер разработки:
```bash
python manage.py runserver
```
