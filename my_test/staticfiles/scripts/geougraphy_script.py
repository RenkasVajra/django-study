import numpy as np
import pandas as pd
import math


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


def creating_html_tables():
    selected_profession = 'Специалист по информационной безопасности'
    csv_file = "C:/Users/Dich/Desktop/VYZ/django-study/vacancies.csv"
    data = pd.read_csv(csv_file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
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
    converted_df['average_salary'] = converted_df[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(
        math.floor).astype(int)
    converted_df['vacancy_rate'] = converted_df['area_name'].map(
        lambda city: len(data[data['area_name'] == city]) / converted_df.shape[0] * 100).round(2).astype(float)
    converted_df_percent = converted_df.rename(columns={'area_name': 'Город'}).sort_values(
        'vacancy_rate', ascending=False).drop(['average_salary'], axis=1).reset_index().drop(['index'], axis=1)
    df1 = converted_df.groupby('area_name')['average_salary'].mean(axis=1).apply(math.floor).astype(int).to_html()
    df2 = converted_df_percent.to_html()
    selected_profession_data = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]
    df3 = selected_profession_data.groupby('area_name')['average_salary'].mean(axis=1).apply(math.floor).astype(int).to_html()
    selected_df_percent = selected_profession_data.rename(columns={'area_name': 'Город'}).sort_values(
        'vacancy_rate', ascending=False).drop(['average_salary'], axis=1).reset_index().drop(['index'], axis=1)
    df4 = selected_df_percent.to_html()
    path = 'C:/Users/Dich/Desktop/VYZ/django-study/my_test/ulearn/templates/includes/'
    f1 = open(path + "geography_dynamic_sal.html", "w", encoding='utf-8')
    f1.write(df1)
    f1.close()
    f2 = open(path + "geography_percent.html", "w", encoding='utf-8')
    f2.write(df2)
    f2.close()
    f3 = open(path + "geography_selected_sal.html", "w", encoding='utf-8')
    f3.write(df3)
    f3.close()
    f4 = open(path + "geography_selected_percent.html", "w", encoding='utf-8')
    f4.write(df4)
    f4.close()


creating_html_tables()