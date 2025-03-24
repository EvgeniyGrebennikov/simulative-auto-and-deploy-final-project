import configparser
import os
import psycopg2
import logging
import re
from datetime import date, datetime, timedelta
from glob import glob

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

# Настройка логирования
## Считываем путь для записи логов
logs_path = config['Logs']['LOGS_PATH']

## Проверяем наличие папки, создаем при необходимости
if not os.path.exists(logs_path):
    os.mkdir(logs_path)

## Настройка логгера
logger = logging.getLogger(__name__)
fileHandler = logging.FileHandler(logs_path + f"{date.today()}.txt", encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s | %(name)s | %(levelname)s: %(message)s",
    handlers=[fileHandler]
)

## Проверка файлов с логами и удаление логов, записанных более 3-х дней назад
files_log = [fl for fl in glob(logs_path + "*") if re.search(r"\d{4}-\d{2}-\d{2}\.log", fl)]

for fl in files_log:
    file_name = re.search(r"\d{4}-\d{2}-\d{2}", fl).group()
    if date.fromisoformat(file_name) <= date.today() - timedelta(days=2):
        os.remove(fl)

class DataBase:
    __instance = None

    # Шаблон Singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    # Конструктор класса для подключения к БД
    def __init__(self, host, port, database, user, password):
        self.connection = psycopg2.connect(
            host = host,
            port = port,
            database = database,
            user = user,
            password = password
        )

    def post(self, query):
        cursor = self.connection.cursor()
        compiler = re.compile(r"insert into (\w+)")
        try:
            cursor.execute(query)
            self.connection.commit()
            logger.info(f"Строка с данными успешно добавлена в таблицу {compiler.search(query).group(1)}")

        except Exception as err:
            self.connection.rollback()
            print(f"Ошибка при загрузке данных в таблицу: {repr(err)}")
            logger.error(f"Ошибка при загрузке данных в таблицу {compiler.search(query).group(1)}: {repr(err)}")

        finally:
            cursor.close()