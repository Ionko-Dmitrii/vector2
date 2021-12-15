import xlsxwriter
import datetime
import pandas as pd
from openpyxl import load_workbook
from decimal import Decimal

import dbworker
chats = dbworker.get_all_chat()

def df(seconds):
    dt = []
    t_id = []
    type = []
    text = []
    if chats !=0:
        for chat in chats:
            if (((datetime.datetime.now().replace(tzinfo=None) - chat.dt.replace(tzinfo=None)).seconds) +
                     (datetime.datetime.now().replace(tzinfo=None) - chat.dt.replace(
                         tzinfo=None)).days * 24 * 3600) < seconds:
                dt.append(chat.dt)
                t_id.append(chat.t_id)
                type.append(chat.type)
                text.append(chat.text)

    data = {
        'Время': dt,
        'ID пользователя': t_id,
        'Тип': type,
        'Текст': text
    }

    df = pd.DataFrame(data).sort_values(by='Время', ascending=True)
    if len(df['Время']) != 0:
        df['Время'] = df['Время'].dt.tz_localize(None)
    return df

def columns(writer):
    workbook= writer.book
    worksheet = writer.sheets['История действий']

    worksheet.set_column('A:Z', width=20, cell_format=workbook.add_format({'align': 'center'}))
