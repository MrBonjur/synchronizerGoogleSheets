from __future__ import annotations

from oauth2client.service_account import ServiceAccountCredentials
from ConfigManager.config import *
import apiclient
import httplib2


class Table:
    def __init__(self):
        # Читаем ключи из файла
        keyfile = ServiceAccountCredentials.from_json_keyfile_name
        credentials = keyfile("./ConfigManager/" + CREDENTIALS_FILE,
                              ['https://www.googleapis.com/auth/spreadsheets',
                               'https://www.googleapis.com/auth/drive']
                              )

        # Авторизуемся в системе
        http_auth = credentials.authorize(httplib2.Http())
        # Выбираем работу с таблицами и 4 версию API
        self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
        self.sheet = self.service.spreadsheets()
        self.values = self.service.spreadsheets().values()

    def get_values(self, ranges: str | list) -> list:
        data = self.values.batchGet(spreadsheetId=SPREADSHEETS_ID, ranges=ranges).execute()['valueRanges'][0]
        if data.get('values') is not None:
            return data['values']
        return []
