import re
import os
import configparser
import pandas as pd
from glob import glob
from data_processing_func import create_cash_receipts_df, return_categories_and_products
from pg_db_connector import DataBase

# Указание отображения кол-ва столбцов датафрейма
pd.set_option('display.max_columns', 40)

# Указание текущего пути
dirname = os.path.dirname(__file__)

# Считываем доступы из config.ini
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))


# Указываем путь к папке data
files_path = config['Files']['FILES_PATH']

# Получаем датафрейм на основе сгенерированных файлов с продажами
cash_receipts_df = create_cash_receipts_df(os.path.join(dirname, files_path))

# Получаем уникальные категории товаров и информацию о продукте (название: цена)
unique_categories, products_info = return_categories_and_products()

# Получаем уникальные чеки (id в строковом виде)
unique_cash_receipts = cash_receipts_df['doc_id'].unique().tolist()

# Генерируем уникальные значения скидок (0-5%)
discounts = list(range(0, 6))

# Создаем объект для подключения к БД (класса DataBase)
host = config['Database']['HOST']
port = config['Database']['PORT']
database = config['Database']['DATABASE']
user = config['Database']['USER']
password = config['Database']['PASSWORD']

db = DataBase(host, port, database, user, password)

# Загружаем данные в таблицу categories (id <PK>, name)
for category in unique_categories:
    query = f"""insert into categories(name)
    values('{category}')"""
    db.post(query)


# Загружаем данные в таблицу products (id <PK>, item, price, category_id <FK>)
for item, category_and_price in products_info.items():
    category, price = category_and_price
    query = f"""insert into products(item, price, category_id)
        values('{item}', {price}, (select id from categories where name = '{category}'))
        """
    db.post(query)


# Загружаем данные в таблицу discounts (id <PK>, discount)
for discount in discounts:
    query = f"""insert into discounts(discount)
    values({discount})"""
    db.post(query)


# Загружаем данные в таблицу receipts (id <PK>, doc)
for doc in unique_cash_receipts:
    query = f"""insert into receipts(doc)
    values('{doc}')"""
    db.post(query)


# Загружаем данные датафрейма (сгенерированных продаж) в таблицу orders (id <PK>, product_id, amount, discount_id <FK>, doc_id <FK>)
for i, row in cash_receipts_df.iterrows():
    date = row['date']
    doc_id = row['doc_id']
    item = row['item']
    category = row['category']
    amount = row['amount']
    price = row['price']
    discount = row['discount']

    query = f"""insert into orders(date, product_id, amount, discount_id, doc_id)
    values('{date}', (select id from products where item = '{item}'),
    ({amount}),
    (select id from discounts where discount = {discount}),
    (select id from receipts where doc = '{doc_id}')
    )"""
    db.post(query)

# Ищем все файлы-csv
files_in_data = [fl for fl in glob(os.path.join(files_path, "*.csv"))]
# Проверяем csv-файлы в папке data, выбираем только кассовые чеки
cash_receipts_files = [fl for fl in files_in_data if re.search(r"\d+_\d+\.csv", fl)]
# Удаляем файлы с кассовыми чеками после их записи в БД
for fl in cash_receipts_files:
    os.remove(fl)


