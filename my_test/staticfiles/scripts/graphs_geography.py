import math
import pandas as pd
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


def creating_plot(df):
    plt.figure(figsize=(16, 8))
    plt.barh(df['Город'], df['Средняя зарплата'])
    plt.tick_params(axis='y', labelrotation=0, labelsize=15)
    plt.tick_params(axis='y', labelright=False, labelleft=True)
    plt.tick_params(axis='x', labelrotation=0, labelsize=15)
    plt.title('Уровень зарплат по городам', fontdict = {'fontsize' : 24})
    plt.tight_layout()
    plt.savefig(f"C:/Users/acer/Desktop/graph_top_20_cities_by_salary.png", dpi=100)
    return


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
    .astype(int).reset_index().dropna(subset=['average_salary']).sort_values('average_salary', ascending=False)
df_by_city = df_by_city[df_by_city.average_salary < 1000000]
df1 = df_by_city.head(20) # зп по городам

count_all = converted_df.groupby('area_name').name.count().reset_index().sort_values(by='name', ascending=False)
df2 = count_all.head(20) # кол-во вакансий по городам

selected_df = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]

selected_df_by_city = selected_df.groupby('area_name').agg({
'average_salary': 'mean'
}).reset_index().dropna(subset=['average_salary']).sort_values('average_salary', ascending=False)
df3 = selected_df_by_city.head(20) # зп по городам для выбранной профессии

selected_count_all = selected_df.groupby('area_name').name.count().reset_index().sort_values(by='name', ascending=False)# доля вакансий по городам для выбранной профессии
df4 = selected_count_all.head(20) # доля вакансий по городам для выбранной профессии

fig, sub = plt.subplots(figsize=(18, 10))
sub.barh(df1['area_name'].to_list(), df1['average_salary'].to_list())
sub.tick_params(axis='x', labelsize=8)
sub.tick_params(axis='y', labelsize=8)
sub.grid(True, axis='y')
sub.set_title('Уровень зарплат по городам')
fig.savefig('../img/geo1.png', dpi=200)
sub.cla()
sub.barh(df2['area_name'].to_list(), df2['name'].to_list())
sub.tick_params(axis='x', labelsize=8)
sub.tick_params(axis='y', labelsize=8)
sub.grid(True)
sub.set_title('Количество вакансий по городам')
fig.savefig('../img/geo2.png', dpi=200)
sub.cla()
sub.barh(df3['area_name'].to_list(), df3['average_salary'].to_list())
sub.tick_params(axis='x', labelsize=8)
sub.tick_params(axis='y', labelsize=8)
sub.set_title('Уровень зарплат по городам для выбранной профессии')
sub.grid(axis='x')
fig.savefig('../img/geo3.png', dpi=200)
sub.cla()
sub.barh(df4['area_name'].to_list(), df4['name'].to_list())
sub.tick_params(axis='x', labelsize=8)
sub.tick_params(axis='y', labelsize=8)
sub.grid(True, axis='y')
sub.set_title('Количество вакансий по городам для выбранной профессии')
fig.savefig('../img/geo4.png', dpi=200)
sub.cla()
plt.tight_layout()
