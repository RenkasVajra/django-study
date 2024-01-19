import math
import pandas as pd

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


selected_profession = 'Специалист по информационной безопасности'
csv_file = "C:/Users/Dich/Desktop/VYZ/django-study/vacancies.csv"
data = pd.read_csv(csv_file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
data.dropna(subset=['area_name', 'salary_from', 'salary_to', 'salary_currency']).reset_index(drop=True)
data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.strftime("%Y-%m")
data = data.replace('RUR', 'RUB')
conv = pd.read_csv('C:/Users/Dich/Downloads/currency.csv')
data = data.dropna(subset=['salary_currency'])
data[['salary_from', 'salary_to']] = data[['salary_from', 'salary_to']].fillna(value=0)
merged_df = pd.merge(data, conv, left_on='published_at', right_on='date', how='left')
converted_df = merged_df.apply(convert_salary, axis=1)
converted_df['salary_currency'] = converted_df['salary_currency'].fillna('RUB')
converted_df = converted_df.fillna(0)
converted_df['published_at'] = pd.to_datetime(converted_df['published_at'], utc=True).dt.year
converted_df['average_salary'] = converted_df[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(math.floor).astype(
int)
converted_df = converted_df[(converted_df.salary_from < 1000000) | (converted_df.salary_to < 1000000)]

df_by_city = converted_df.groupby('area_name').agg({'average_salary': 'mean'})\
    .reset_index().dropna(subset=['average_salary']).sort_values('average_salary', ascending=False)
df_by_city['average_salary'] = df_by_city['average_salary'].apply(math.floor).astype(int)
df1 = df_by_city.rename(columns={'area_name': 'Город', 'average_salary': 'Средняя зарплата'}).head(20).to_csv(index=False) # зп по городам
df_by_city = df_by_city[(df_by_city.average_salary < 1000000)]

count_all = converted_df.groupby('area_name').name.count().reset_index().sort_values(by='name', ascending=False)
df2 = count_all.head(20).rename(columns={'area_name': 'Город', 'name': 'Количество вакансий'}).to_csv(index=False) # кол-во вакансий по городам

selected_df = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]

selected_df_by_city = selected_df.groupby('area_name').agg({
    'average_salary': 'mean'
    }).reset_index().dropna(subset=['average_salary']).sort_values('average_salary', ascending=False)
selected_df_by_city['average_salary'] = selected_df_by_city['average_salary'].apply(math.floor).astype(int)
df3 = selected_df_by_city.rename(columns={'area_name': 'Город', 'average_salary': 'Средняя зарплата'}).head(20).to_csv(index=False) # зп по городам для выбранной профессии

selected_count_all = selected_df.groupby('area_name').name.count().reset_index().sort_values(by='name', ascending=False)
df4 = selected_count_all.rename(columns={'area_name': 'Город', 'name': 'Количество вакансий'}).head(20).to_csv(index=False) # доля вакансий по городам для выбранной профессии
path = 'C:/Users/Dich/Desktop/VYZ/django-study/my_test/staticfiles/geography/'
f1 = open(path + "geo_salary_all.csv", "w", encoding='utf-8')
f1.write(df1)
f1.close()
f2 = open(path + "geo_count_all.csv", "w", encoding='utf-8')
f2.write(df2)
f2.close()
f3 = open(path + "geo_salary_prof.csv", "w", encoding='utf-8')
f3.write(df3)
f3.close()
f4 = open(path + "geo_count_prof.csv", "w", encoding='utf-8')
f4.write(df4)
f4.close()
