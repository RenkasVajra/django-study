import requests
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Vacancy


def index_page(request):
    return render(request, 'index.html')


def demand(request):
    return render(request, 'demand.html', )


def geography(request):
    return render(request, 'geography.html', )


def skills(request):
    return render(request, 'skills.html', )


def last_vacancies(request):
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
    vacancies_data = data.get('items', [])
    print(data)
    print(vacancies_data)
    # Обработка данных о вакансиях
    vacancies_list = []
    for vacancy_data in vacancies_data:
        if not (None in vacancy_data.values()):
            vacancy = Vacancy()
            vacancy.title = vacancy_data.get('name')
            vacancy.description = get_vacancy_description(vacancy_data.get('url'))
            vacancy.skills = get_vacancy_skills(vacancy_data.get('url'))
            vacancy.company = vacancy_data.get('employer').get('name')
            vacancy.salary = vacancy_data.get('salary').get('from')
            vacancy.area_name = vacancy_data.get('area').get('name')
            vacancy.published_at = datetime.strptime(vacancy_data.get('published_at'), '%Y-%m-%dT%H:%M:%S%z')

            vacancies_list.append(vacancy)
            print(vacancy.title, vacancy.salary)
    # Сохранение вакансий в базе данных
    Vacancy.objects.bulk_create(vacancies_list)

    # Получение и отображение списка последних вакансий
    last_vacancies = Vacancy.objects.order_by('-published_at')[:10]

    return render(request, 'last_vacancies.html', {'last_vacancies': last_vacancies})


def get_vacancy_description(vacancy_url):
    # Отправка GET-запроса к API HH для получения данных о вакансии
    response = requests.get(vacancy_url)
    vacancy_data = response.json()

    return vacancy_data['description']


def get_vacancy_skills(vacancy_url):
    # Отправка GET-запроса к API HH для получения данных о вакансии
    response = requests.get(vacancy_url)
    vacancy_data = response.json()
    skills = []

    for skill_data in vacancy_data['key_skills']:
        skills.append(skill_data['name'])

    return ', '.join(skills)

