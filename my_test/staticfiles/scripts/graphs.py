import pandas as pd
import math
import matplotlib.pyplot as plt


def convert_salary(row):
    if row['salary_currency'] != 'RUB':
        currency = row['salary_currency']
        salary_from = row['salary_from']
        salary_to = row['salary_to']
        exchange_rate = row[currency]

        if pd.notnull(salary_from):
            salary_from_rub = salary_from * exchange_rate
            row['salary_from'] = salary_from_rub

        if pd.notnull(salary_to):
            salary_to_rub = salary_to * exchange_rate
            row['salary_to'] = salary_to_rub

    return row


def demand():
    selected_profession = 'Специалист по информационной безопасности'
    csv_file = "C:/Users/Dich/Desktop/VYZ/django-study/vacancies.csv"
    data = pd.read_csv(csv_file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])
    data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.strftime("%Y-%m")
    data = data.replace('RUR', 'RUB')
    conv = pd.read_csv('C:/Users/Dich/Downloads/currency.csv')
    data = data.dropna(subset=['salary_currency'])
    data[['salary_from', 'salary_to']] = data[['salary_from', 'salary_to']].fillna(value=0)
    merged_df = pd.merge(data, conv, left_on='published_at', right_on='date', how='left')

    converted_df = merged_df.apply(convert_salary, axis=1)
    converted_df['salary_currency'] = converted_df['salary_currency'].fillna('RUB')
    converted_df = converted_df.fillna(0)
    converted_df['Год'] = pd.to_datetime(converted_df['published_at'], utc=True).dt.year
    converted_df['average_sal'] = converted_df[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(
        math.floor).astype(
        int)
    years = sorted(converted_df['Год'].unique())
    average_salary_all = converted_df.groupby('Год')['average_sal'].mean().apply(math.floor).astype(
        int).to_frame()  # зп для всех
    selected_profession_data = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]
    selected_salary_all = selected_profession_data.groupby('Год')[
        'average_sal'].mean().astype(
        int).to_frame()  # зп для профессии

    years_df = converted_df.groupby('Год')['name'].count().reset_index()  # кол-во вакансии
    vacancies_all_count = years_df['name'].tolist()
    vacancies_count_profession_by_year = selected_profession_data.groupby('Год')['name'].count().reset_index()
    vacancies_count_profession_by_year = vacancies_count_profession_by_year.rename(
        columns={'name': 'count'})  # кол-во выбранная вакансия
    fig, sub = plt.subplots(figsize=(16, 8))
    sub.bar(years, average_salary_all['average_sal'].to_list(), width=0.4)
    sub.grid(True, axis='y')
    plt.rcParams['font.size'] = 8
    sub.set_title('Уровень зарплат по годам')
    sub.set_xticks([year + 0.2 for year in years])
    sub.set_xticklabels(years, )
    fig.savefig('figure1.png')
    sub.clf()
    sub.bar(years, years_df['name'].to_list(), width=0.4)
    sub.grid(True)
    sub.set_title('Количество вакансий по годам')
    sub.set_xticks([year + 0.2 for year in years])
    sub.set_xticklabels(years, )
    fig.savefig('figure2.png')
    sub.clf()
    selected_profession_years = sorted(selected_profession_data['Год'].unique())
    sub.bar(selected_profession_years, selected_salary_all['average_sal'].to_list(), width=0.4)
    sub.set_title('Уровень зарплат по годам для выбранной профессии')
    sub.grid(axis='x')
    sub.set_xticks([year + 0.2 for year in years])
    sub.set_xticklabels(years, )
    fig.savefig('figure3.png')
    sub.clf()
    sub.bar(selected_profession_years, vacancies_count_profession_by_year['count'].to_list(), width=0.4)
    sub.grid(True, axis='y')
    sub.set_title('Количество вакансий по годам для выбранной профессии')
    sub.set_xticks([year + 0.2 for year in years])
    sub.set_xticklabels(years, )
    fig.savefig('figure4.png')
    sub.clf()
    plt.tight_layout()
    return sub


demand()
