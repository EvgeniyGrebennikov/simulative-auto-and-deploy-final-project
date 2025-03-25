import random
import csv
import string
import pandas as pd
import configparser
import os
from collections import defaultdict
from datetime import date, timedelta

pd.set_option('display.max_columns', 40)

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

files_path = config['Files']['FILES_PATH']

if not os.path.exists(files_path):
    os.mkdir(files_path)

def generate_data(daily_receipts, shops_list, cash_registers):
    with open(os.path.join(dirname, 'products.csv'), 'r', encoding='utf-8') as file:
        # Сохраним в data список всех товаров, которые есть в продаже
        data = list(csv.reader(file))[1:]

        # Итоговый словарь с информацией по чекам
        cash_receipts_info = defaultdict(list)

        # Пройдемся по списку сгенерированных магазинов
        for shop_num in shops_list:
            # Сгенерируем текущее кол-во позиций в чеке
            receipt_positions = random.randint(1, 7)

            # Определим товары, которые были куплены с учетом кол-ва позиций чека (receipt_positions)
            current_items = random.choices(data, k=receipt_positions)

            # Определим номер кассы для чека (всего имеется 5 касс)
            cash_num = random.choice(cash_registers)

            # Сгенерируем id чека
            doc_id = ["".join(random.choices(list(string.ascii_letters + string.digits), k=16))] * receipt_positions
            item = list(map(lambda elem: elem[1], current_items))

            category = list(map(lambda elem: elem[0], current_items))

            amount = [random.randint(1, 15) for _ in range(receipt_positions)]

            price = list(map(lambda elem: elem[2], current_items))

            discount = [random.randint(0, 5) for _ in range(receipt_positions)]

            shop_num = [shop_num] * receipt_positions
            cash_num = [cash_num] * receipt_positions

            cash_receipts_info['date'].extend([(date.today() - timedelta(days=1)).isoformat()] * len(current_items))
            cash_receipts_info['doc_id'].extend(doc_id)
            cash_receipts_info['item'].extend(item)
            cash_receipts_info['category'].extend(category)
            cash_receipts_info['amount'].extend(amount)
            cash_receipts_info['price'].extend(price)
            cash_receipts_info['discount'].extend(discount)
            cash_receipts_info['shop_num'].extend(shop_num)
            cash_receipts_info['cash_num'].extend(cash_num)

        return cash_receipts_info

# Сгенерируем количество чеков за день. Будем считать, что в день от 10 до 50 покупок
daily_receipts = random.randint(10, 50)
# Определим номера магазинов, в которых были покупки. Кол-во магазинов равно кол-ву чеков daily_receipts
shops_list = [random.randint(1, 15) for _ in range(daily_receipts)]
# Укажем, что в каждом из магазинов по 5 кассовых аппаратов
cash_registers = list(range(1, 6))

result_gen = generate_data(daily_receipts, shops_list, cash_registers)

cash_receipts_df = pd.DataFrame(result_gen)

shop_nums = sorted(cash_receipts_df['shop_num'].unique().tolist())
for shp in shop_nums:
    cash_nums = sorted(cash_receipts_df[cash_receipts_df['shop_num'] == shp]['cash_num'].unique().tolist())
    for csh in cash_nums:
        current_df = cash_receipts_df[(cash_receipts_df['shop_num'] == shp) & (cash_receipts_df['cash_num'] == csh)]
        current_df.loc[:, :'discount'].to_csv(os.path.join(dirname, files_path, f"{shp}_{csh}.csv"), index=False)