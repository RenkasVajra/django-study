from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('demand/', views.demand, name='demand'),
    path('geography/', views.geography, name='geography'),
    path('skills/', views.skills, name='skills'),
    path('vacancies/', views.last_vacancies, name='last_vacancies'),
]