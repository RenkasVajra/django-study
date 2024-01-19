# issecurityaoo

### Проект доступен по адресу:  
[http://84.252.134.130/](http://www.issecurityaoo.ru/)


## Описание

Приложение issecurityaoo - сайт, на котором размещена информация о вакансии 
"Специалист по информационной безопасности", взятая с открытого ресура HH.ru.
На сайте размещены 5 страниц - главная, востребованность, география, навыки
и последние вакансии

Проект был выполнен в качестве дипломного задания в Яндекс Практикум.

## Стек технологий
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Nginx](https://nginx.org/)
- [Reg.ru](https://www.reg.ru/)
- [GitHub Actions](https://github.com/features/actions)

## Установка проекта 

- Зайдите на хост Reg.ru и создайте виртуальное окружение vvv/home \
  `ls -la /opt/python/*/bin/python`
  `/opt/python/python-3.9.0/bin/python -m venv djangoenv`

- Активируйте виртуальное окружение \
  `source djangoenv/bin/activate`
- Склонируйте репозиторий в директорию django-study \
`git clone https://github.com/RenkasVajra/django-study`.
- Установите нужные пакеты \
  `pip3 install -r requirements.txt`

- Примените миграции \
  python manage.py migrate`

- Соберите статику \
`python manage.py collectstatic --no-input`

- Создайте суперпользователя \
`python manage.py createsuperuser`

- Добавьте в settings.py головного приложения имя вашего домена и его псевдонимы \
  `ALLOWED_HOSTS = ['issecurityaoo.ru', 'www.issecurityaoo.ru', '127.0.0.1', 'localhost']`

- В корневой директории сайта(issecurityaoo.ru) создайте файл passenger_wsgi.py и внесите следующий код: \
  `import os, sys
  sys.path.insert(0, '/var/www/u2439865/data/www/issecurityaoo.ru/my_test')
  sys.path.insert(1, '/var/www/u2439865/data/djangoenv/lib/python3.9/site-packages')
  os.environ['DJANGO_SETTINGS_MODULE'] = 'my_test.settings'
  from django.core.wsgi import get_wsgi_application
  application = get_wsgi_application()
    где u2439865 - логин хоста,
    issecurityaoo.ru - название директории сайта,
    my_test - головное приложение`
