from __future__ import annotations

import threading

import requests
import psycopg2
import time
import datetime

from ConfigManager.config import *
from Utils import converter

from Utils import table


table = table.Table()
dollars_to_rubs = converter.Converter("USD", "RUB")
temp_check_time = []


class PostgreSQL:
    def __init__(self):
        self.database = psycopg2.connect(database=POSTGRESQL_DATABASE,
                                         user=POSTGRESQL_USER,
                                         password=POSTGRESQL_PASSWORD,
                                         host=POSTGRESQL_HOST,
                                         port=POSTGRESQL_PORT)
        self.database.autocommit = True
        self.cursor = self.database.cursor()
        print("PostgreSQL successfully connected!")
        threading.Thread(target=self.checker_date).start()

    # checks for expired date
    def checker_date(self):
        time.sleep(10)
        while True:
            self.cursor.execute(f"SELECT ID, DELIVERY_TIME, ORDER_ID FROM {POSTGRESQL_NAME_TABLE}")
            array_dates = self.cursor.fetchall()

            for d in array_dates:
                if check_time(d[0], d[1]):  # d[0] - 12, d[1] - 02.08.2022
                    text = f"У заказа номер {d[2]} просрочился срок доставки!"
                    send_notification(notification_text=text)  # send to telegram

            time.sleep(60)

    def create_table(self):
        create_table = f'''CREATE TABLE if not exists {POSTGRESQL_NAME_TABLE} (
            ID INT,
            ORDER_ID INT,
            PRICE_DOLLARS INT,
            PRICE_RUBS INT,
            DELIVERY_TIME VARCHAR(20)
        );
        '''
        self.cursor.execute(create_table)

    def init_data(self):
        users = []
        values = table.get_values(f"{LIST_NAME}!A:D")[1:]

        for value in values:
            new_rub = dollars_to_rubs.convert(value[2])  # value[2] - dollars
            temp_date = value[3]  # date
            value[3] = new_rub  # rubs
            value.append(temp_date)
            users.append(tuple(value))

        user_records = ", ".join(["%s"] * len(users))
        add = f"""INSERT INTO {POSTGRESQL_NAME_TABLE} 
              (ID, ORDER_ID, PRICE_DOLLARS, PRICE_RUBS, DELIVERY_TIME)
              VALUES {user_records}
        """

        self.cursor.execute(add, users)
        print("Successfully initialized!")

    def update_data(self, data: list):
        row_id = data[0]
        order_id = check_null(data[1])
        price_dollars = check_null(data[2])
        delivery_time = check_null(data[3])

        if price_dollars != 'NULL':
            price_rubs = dollars_to_rubs.convert(check_null(data[2]))
        else:
            price_rubs = 'NULL'

        update_data = f'''UPDATE {POSTGRESQL_NAME_TABLE}
                SET ORDER_ID = {order_id}, 
                PRICE_DOLLARS = {price_dollars}, 
                PRICE_RUBS = {price_rubs}, 
                DELIVERY_TIME = {delivery_time}
                WHERE ID = '{row_id}';
        '''

        self.cursor.execute(update_data)

    def close_connection(self):
        self.database.close()


def check_time(data_id: str, date_time: str) -> bool:
    if data_id not in temp_check_time:
        my_date = datetime.datetime.strptime(date_time, '%d.%m.%Y')
        now_time = datetime.datetime.now()
        temp_check_time.append(data_id)
        if now_time > my_date:
            return True

    return False


def send_notification(notification_text: str):
    requests.get(f"https://api.telegram.org/bot{token_telegram}"
                 f"/sendMessage?chat_id={channel_id}"
                 f"&text={notification_text}")


def is_init() -> bool:
    if open("./ConfigManager/init", "r").read() == "False":
        return False
    else:
        return True


def set_init(value: bool):
    with open("./ConfigManager/init", "w") as file_init:
        file_init.write(str(value))


def check_null(value: int | str) -> int | str:
    if isinstance(value, str):
        if value.count(".") == 2:
            return "'" + value + "'"

    if not value:
        return 'NULL'

    return value
