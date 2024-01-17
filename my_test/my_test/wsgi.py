"""
WSGI config for my_test project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application


# -*- coding: utf-8 -*-
sys.path.insert(0, '/var/www/u2439865/data/www/issecurityaoo.ru/django-study/my_test')
sys.path.insert(1, '/var/www/u2439865/data/www/issecurityaoo.ru/django-study/my_test/djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_test.settings'
application = get_wsgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_test.settings')

application = get_wsgi_application()
