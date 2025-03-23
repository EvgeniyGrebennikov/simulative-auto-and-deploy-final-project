import configparser
import os
import psycopg2

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

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
        try:
            cursor.execute(query)
            self.connection.commit()

        except Exception as err:
            self.connection.rollback()
            print(f"Ошибка при загрузке данных в таблицу: {repr(err)}")

        finally:
            cursor.close()