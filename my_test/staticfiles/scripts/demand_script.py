import numpy as np
import pandas as pd
import math


def demand():
    selected_profession = 'Специалист по информационной безопасности'
    csv_file = "C:/Users/Dich/Desktop/VYZ/django-study/vacancies.csv"
    data = pd.read_csv(csv_file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])
    data = data.fillna(0)
    data['Год'] = pd.to_datetime(data['published_at'], utc=True).dt.year
    data['average_sal'] = data[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(math.floor).astype(
        int)
    years = sorted(data['Год'].unique())
    average_salary_all = data.groupby('Год')['average_sal'].mean().apply(math.floor).astype(
        int).to_frame()  # зарплата по годам
    selected_profession_data = data[data.name.str.contains(selected_profession, na=False, case=False)]
    selected_salary_all = selected_profession_data.groupby('Год')[
        'average_sal'].mean().astype(
        int).to_frame()  # зарплата по годам выбранная

    years_df = data.groupby('Год')['name'].count().reset_index()  # кол-во вакансий по годам
    vacancies_all_count = years_df['name'].tolist()
    vacancies_count_profession_by_year = selected_profession_data.groupby('Год')['name'].count().reset_index()
    vacancies_count_profession_by_year = vacancies_count_profession_by_year.rename(
        columns={'name': 'count'})  # кол-во вакансий по годам для профессии
    path = 'C:/Users/Dich/Desktop/VYZ/django-study/my_test/ulearn/templates/includes/'
    df1 = average_salary_all.reset_index().to_html()  # зп для всех
    df2 = years_df.set_index('Год').rename(
        columns={'name': 'vacancy_count'}).reset_index().to_html()  # кол-во вакансии
    df3 = selected_salary_all.reset_index().to_html() # зп для профессии
    df4 = vacancies_count_profession_by_year.to_html()  # выбранная вакансия
    f1 = open(path + "demand_salary_all.html", "w")
    f1.write(df1)
    f1.close()
    f2 = open(path + "vacancy_count_all.html", "w")
    f2.write(df2)
    f2.close()
    f3 = open(path + "demand_salary_prof.html", "w")
    f3.write(df3)
    f3.close()
    f4 = open(path + "vacancy_count_prof.html", "w")
    f4.write(df4)
    f4.close()
    return


demand()
