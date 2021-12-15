import xlsxwriter
import datetime
import pandas as pd
from openpyxl import load_workbook
from decimal import Decimal

import dbworker

supports = dbworker.get_all_support()

def df(seconds):
    connect_id = []
    t_id = []
    admin_id = []
    from_who = []
    time = []
    message = []
    if supports != 0:
        for support in supports:
            if (((datetime.datetime.now().replace(tzinfo=None) - support.time.replace(tzinfo=None)).seconds)+
                (datetime.datetime.now().replace(tzinfo=None) - support.time.replace(tzinfo=None)).days * 24*3600) < seconds:
                connect_id.append(support.connect_id)
                t_id.append(support.t_id)
                admin_id.append(support.admin_id)
                time.append(support.time)
                message.append(support.message)
                from_who.append(support.from_who)

    df = pd.DataFrame({
        'ID подключения': connect_id,
        'ID пользователя': t_id,
        'ID администратора': admin_id,
        'Время соообщения': time,
        'Сообщение': message,
        'Кто отправил': from_who
    })
    if len(df['ID подключения']) != 0:
        df['Время соообщения'] = df['Время соообщения'].dt.tz_localize(None)
    df2 = df.sort_values(['ID подключения', 'Время соообщения'])
    return df2

def columns(writer):
    workbook= writer.book
    worksheet = writer.sheets['Support']

    worksheet.set_column('A:Z', width=17, cell_format=workbook.add_format({'align': 'center'}))
    worksheet.set_column('C:C', 20)