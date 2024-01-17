from django.contrib.auth.models import AbstractUser
from django.db import models


class SiteUser(AbstractUser):
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128, null=True, unique=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  # Укажите поле, используемое в качестве уникального идентификатора
    REQUIRED_FIELDS = ['email']

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'site_users'
