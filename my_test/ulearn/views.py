from django.shortcuts import render, redirect
import pandas as pd
import json
import math

def index_page(request):
    return render(request, 'index.html')


def demand(request):
    selected_profession = 'Специалист по информационной безопасности'
    csv_file = 'vacancies.csv'
    data = pd.read_csv(csv_file, names=['name', 'salary_from', 'salary_to', 'salary_currency', 'Город', 'Год'])
    data.dropna()
    data['Год'] = pd.to_datetime(data['Год'], utc=True).dt.year
    data['average_sal'] = data[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(math.floor).astype(
        int)
    years = sorted(data['Год'].unique())
    average_salary_all = data.groupby('Год')['average_sal'].mean().to_frame()  # зарплата по годам
    selected_profession_data = data[data.name.str.contains(selected_profession, na=False, case=False)]
    selected_salary_all = selected_profession_data.groupby('Год')[
        'average_sal'].mean().to_frame()  # зарплата по годам выбранная

    years_df = data.groupby('Год')['name'].count().reset_index()  # кол-во вакансий по годам
    vacancies_all_count = years_df['name'].tolist()
    vacancies_count_profession_by_year = selected_profession_data.groupby('Год')['name'].count().reset_index()
    vacancies_count_profession_by_year = vacancies_count_profession_by_year.rename(
        columns={'name': 'Кол-во вакансий'})  # кол-во вакансий по годам для профессии
    df1 = json.loads(average_salary_all.reset_index().to_json())
    df2 = json.loads(selected_salary_all.reset_index().to_json())
    df3 = json.loads(years_df.set_index('Год').rename(
        columns={'name': 'Кол-во вакансий'}).reset_index().to_json())
    df4 = json.loads(vacancies_count_profession_by_year.to_json())
    context = {'d1': df1, 'd2': df2, 'd3': df3, 'd4': df4}
    return render(request, 'demand.html', context)

