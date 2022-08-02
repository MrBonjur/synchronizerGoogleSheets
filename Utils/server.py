import os
import sys

from vk_api.bot_longpoll import VkBotLongPoll
import threading
import vk_api
import time

from Utils import postgresql
from Utils import table
from ConfigManager import config


table = table.Table()
postgreSQL = postgresql.PostgreSQL()


class Server:
    def __init__(self):
        vk_session = vk_api.VkApi(token=config.token_vk)
        self.long_poll = VkBotLongPoll(vk_session, config.id_group)

        # if no exists table in PostgreSQL
        if not postgresql.is_init():
            postgreSQL.create_table()
            postgreSQL.init_data()
            postgresql.set_init(True)

    # get messages in vk
    def start(self):
        for event in self.long_poll.listen():
            message = str(event.message.text)

            if "Changed value:" in message:
                coordinates = message.split()[2]

                # if type = A1
                if ":" not in coordinates:
                    x = coordinates[1:]
                    array_value = table.get_values(f"{config.LIST_NAME}!{x}:1")[-1:][0]
                    postgreSQL.update_data(array_value)

                # if type = A1:B6
                elif ":" in coordinates:
                    x = int(coordinates.split(":")[0][1:])
                    y = int(coordinates.split(":")[1][1:])

                    for i in range(x - 1, y):
                        postgreSQL.update_data([i, 0, 0, 0])


def starter():
    os.execv(sys.executable, [sys.executable] + sys.argv)  # restart server


def check_restart():
    time.sleep(config.RESTART_DELAY)
    threading.Thread(target=starter).start()
    os.kill(os.getpid(), 0xDEADC0DE)
