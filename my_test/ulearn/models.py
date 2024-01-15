from django.db import models


class SiteUser(models.Model):
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)

    def get_name(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        db_table = 'site_users'


class Vacancy(models.Model):
    title = models.TextField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', max_length=3000)
    skills = models.CharField(verbose_name='Навыки', max_length=255)
    company = models.CharField(verbose_name='Компания', max_length=255)
    salary = models.CharField(verbose_name='Зарплата', max_length=25)
    area_name = models.CharField(verbose_name='Местоположение', max_length=255)
    published_at = models.TextField(verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        db_table = 'vacancies'
