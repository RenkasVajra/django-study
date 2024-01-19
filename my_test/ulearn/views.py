import requests
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Vacancy, Demand, Geography, Skills
import json
import re


def index_page(request):
    return render(request, 'index.html')


def demand(request):
    demanded = Demand.objects.all()
    return render(request, 'demand.html', context={'demand': demanded})


def geography(request):
    geographies = Geography.objects.all()
    return render(request, 'geography.html', context={'geography': geographies})


def skills(request):
    skill = Skills.objects.all()
    return render(request, 'skills.html', context={'skills': skill})


def last_vacancies(request):
    Vacancy.objects.all().delete()
    # API HH URL
    hh_api_url = 'https://api.hh.ru/vacancies'

    # Заголовок запроса
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Параметры запроса: профессия и период (24 часа назад до текущего момента)
    profession = 'Специалист по информационной безопасности'  # Здесь нужно указать выбранную профессию
    period = 24

    date_from = datetime.now() - timedelta(hours=period)

    # Опции запроса
    params = {
        'text': profession,
        'date_from': date_from.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'per_page': 10,
        'order_by': 'publication_time'
    }

    # Отправка GET-запроса к API HH
    response = requests.get(hh_api_url, params=params, headers=headers)
    data = response.json()
    vacancies_data = json.loads(response.content)
    # Обработка данных о вакансиях
    vacancies_list = []
    for vacancy_data in vacancies_data['items']:
        salary = vacancy_data['salary']
        key_skills = get_vacancy_skills(vacancy_data['url'])
        if salary:
            if salary['from'] and salary['to']:
                result_salary = f'{salary["from"]} - {salary["to"]} ({salary["currency"]})'
            elif salary['from']:
                result_salary = f'{salary["from"]}  ({salary["currency"]})'
            else:
                result_salary = f'{salary["to"]}  ({salary["currency"]})'
        else:
            result_salary = 'Зарплата не указана'
        if key_skills:
            result_skills = key_skills
        else:
            result_skills = 'Навыки не указаны'
        vacancy = Vacancy()
        vacancy.title = vacancy_data['name']
        vacancy.description = get_vacancy_description(vacancy_data['url'])
        vacancy.skills = result_skills
        vacancy.company = vacancy_data['employer']['name']
        vacancy.salary = result_salary
        vacancy.area_name = vacancy_data['area']['name']
        vacancy.published_at = datetime.strptime(vacancy_data['published_at'], '%Y-%m-%dT%H:%M:%S%z')

        vacancies_list.append(vacancy)

    for i in vacancies_list:
        if Vacancy.objects.filter(
                title=i.title,
                description=i.description,
                company=i.company,
                skills=i.skills,
                area_name=i.area_name
        ).exists():
            vacancies_list.remove(i)
    # Сохранение вакансий в базе данных
    Vacancy.objects.bulk_create(vacancies_list)

    # Получение и отображение списка последних вакансий
    last_vacancies = Vacancy.objects.order_by('-published_at')[:10]

    return render(request, 'last_vacancies.html', {'last_vacancies': last_vacancies})


def get_vacancy_description(vacancy_url):
    # Отправка GET-запроса к API HH для получения данных о вакансии
    response = requests.get(vacancy_url)
    vacancy_data = response.json()

    return re.sub(r'<[^>]+>', '', vacancy_data['description']).replace('&quot;', '.')


def get_vacancy_skills(vacancy_url):
    # Отправка GET-запроса к API HH для получения данных о вакансии
    response = requests.get(vacancy_url)
    vacancy_data = response.json()
    skills = []

    for skill_data in vacancy_data['key_skills']:
        skills.append(skill_data['name'])

    return ', '.join(skills)
