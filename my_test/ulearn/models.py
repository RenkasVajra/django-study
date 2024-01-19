from django.db import models
import pandas as pd


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


class Demand(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение',upload_to='staticfiles', null=True)
    table = models.FileField(verbose_name='Таблица',max_length=3000, null=True)

    def display_text_file(self):
        df = pd.read_csv(self.table.path, encoding='utf-8')
        json_records = df.to_html()
        return json_records

    class Meta:
        verbose_name = 'Востребованность'
        verbose_name_plural = 'Востребованности'
        db_table = 'demand'


class Geography(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение',upload_to='staticfiles', null=True)
    table = models.FileField(verbose_name='Таблица',max_length=3000, null=True)

    def display_text_file(self):
        df = pd.read_csv(self.table.path, encoding='utf-8')
        json_records = df.to_html()
        return json_records

    class Meta:
        verbose_name = 'География'
        verbose_name_plural = 'География'
        db_table = 'geography'


class Skills(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение',upload_to='staticfiles', null=True)
    table = models.FileField(verbose_name='Таблица',max_length=3000, null=True)

    def display_text_file(self):
        df = pd.read_csv(self.table.path, encoding='utf-8')
        json_records = df.to_html()
        return json_records

    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = 'Навыки'
        db_table = 'skills'
