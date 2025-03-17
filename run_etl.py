import re
import os
import configparser
import pandas as pd
from pg_db_connector import DataBase
from glob import glob

pd.set_option('display.max_columns', 10)

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

# Создаем датафрейм на основе csv файлов кассовых чеков
def create_df(files_path):
    files_in_data = [fl for fl in glob(files_path + "*.csv")]

    # Проверяем файлы в папке data, выбираем только кассовые чеки
    cash_receipts_files = [fl for fl in files_in_data if re.search(r"data\\\d{1,}\_\d\.csv", fl)]

    # Создаем датафрейм и объединяем его со считываемыми данными
    result_df = pd.DataFrame()

    for fl in cash_receipts_files:
        current_df = pd.read_csv(fl)
        result_df = pd.concat([result_df, current_df])

    # Сбрасываем индексы датафрейма
    result_df.reset_index(inplace=True)
    return result_df

# Указываем путь к папке data
files_path = config['Files']['FILES_PATH']
receipts_df = create_df(files_path)

# Создаем объект класса Database
host = config['Database']['HOST']
port = config['Database']['PORT']
database = config['Database']['DATABASE']
user = config['Database']['USER']
password = config['Database']['PASSWORD']

db = DataBase(host, port, database, user, password)

categories_insert_query = """
    insert into categories (name)
    values(%s)
    ON CONFLICT (name) DO NOTHING
"""

receipts_insert_query = """
    insert into receipts (doc)
    values(%s)
    ON CONFLICT (doc) DO NOTHING
"""

discounts_insert_query = """
    insert into discounts (discount)
    values(%s)
    ON CONFLICT (discount) DO NOTHING
"""

products_insert_query = """
    insert into products (item, price, category_id)
    values(%s, %s, %s)
"""



for i, row in receipts_df.iterrows():
    db.post(categories_insert_query, (row['category'],))
    db.post(receipts_insert_query, (row['doc_id'],))
    db.post(discounts_insert_query, (row['discount'],))



