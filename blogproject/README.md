# Django-проект: blog + crud + reports

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py test                       # blog: 1 тест падает намеренно (лайки)
    python manage.py export_tests_docx          # все тесты -> test_report.docx
    python manage.py runserver                  # /  (блог)   /items/  (CRUD)

## Приложения
- blog    — List/Detail, поле likes, тесты (лаба 1)
- crud    — готовый CRUD-шаблон (Item): list, detail, create, update, delete + 13 тестов
- reports — команда export_tests_docx (запускает тесты и пишет их в Word)

## Как использовать crud на следующей лабе
1. Откройте crud/models.py: переименуйте Item (например, в Product) и замените поля по заданию.
2. crud/forms.py: в fields перечислите те же поля.
3. Переименуйте Item -> Product в views.py, admin.py, tests.py, urls.py (Ctrl+Shift+H / "Заменить во всех файлах").
4. Если приложение переименовываете: имя папки, app_name в urls.py, 'crud' в INSTALLED_APPS и include() в config/urls.py.
5. Удалите старую миграцию crud/migrations/0001_initial.py и db.sqlite3, затем:
       python manage.py makemigrations
       python manage.py migrate
6. python manage.py test — все тесты должны пройти. Затем:
       python manage.py export_tests_docx -o lab2.docx

## Параметры export_tests_docx
    python manage.py export_tests_docx crud       # только приложение crud
    python manage.py export_tests_docx --no-run   # только список и код, без запуска
    python manage.py export_tests_docx -o file.docx

## Чтобы тест лайков прошёл (blog/views.py)
    from django.db.models import F
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Blog.objects.filter(pk=obj.pk).update(likes=F('likes') + 1)
        obj.refresh_from_db()
        return obj
