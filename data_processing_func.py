import re
import os
import configparser
import pandas as pd
from glob import glob

pd.set_option('display.max_columns', 40)

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

# Функция для создания датафрейма по сгенерированным продажам (на основе csv файлов кассовых чеков)
def create_cash_receipts_df(files_path):
    # Выбираем все csv-файлы
    files_in_data = [fl for fl in glob(files_path + "*.csv")]

    # Проверяем csv-файлы в папке data, выбираем только кассовые чеки
    cash_receipts_files = [fl for fl in files_in_data if re.search(r"data\\\d{1,}\_\d\.csv", fl)]

    # Создаем пустой датафрейм и объединяем его со считываемыми данными
    result_df = pd.DataFrame()

    # Пробегаемся по файлам с чеками и объединяем данные в общий датафрейм
    for fl in cash_receipts_files:
        current_df = pd.read_csv(fl)
        result_df = pd.concat([result_df, current_df])

    # Сбрасываем индексы в итоговом датафрейме
    result_df = result_df.reset_index().drop('index', axis=1)
    return result_df


# Функция для получения уникальных категорий и товаров (для загрузки в таблицы БД categories и products)
def return_categories_and_products():
    df = pd.read_csv('products.csv')
    categories_name = df['category'].unique().tolist()
    products_info_dict = {product: (category, price) for product, category, price in zip(df['product'], df['category'], df['price'])}
    return categories_name, products_info_dict