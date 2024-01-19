import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

currencies = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]
cols = ["date", "BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]

dates = pd.date_range(start=datetime.datetime(2003, 1, 1), end=datetime.datetime(2023, 12, 1), freq='MS').tolist()
dates_as_string = [date.strftime('%d/%m/%Y') for date in dates]
data = []
for i in range(len(dates)):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={dates_as_string[i]}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    valutes = soup.find_all('Valute')
    date_data = {}
    for valute in valutes:
        charcode = valute.CharCode.text
        value = valute.VunitRate.text.replace(',', '.')
        date_data[charcode] = value
    row = [dates[i].strftime('%Y-%m')]
    for currency in currencies:
        if currency in list(date_data.keys()):
            row.append(date_data[currency])
        else:
            row.append(None)
    data.append(row)
df = pd.DataFrame(data, columns=cols)
df.to_csv("currency.csv", index=False)
