import xlsxwriter
import datetime
import pandas as pd
from openpyxl import load_workbook
from decimal import Decimal

import dbworker

codes = dbworker.get_all_codes()
def df(seconds):
    code_id = []
    id = []
    create_dt = []
    end_dt = []
    type = []
    amount = []
    code_text = []
    status = []

    if codes != 0:
        for code in codes:
            if code.status == 2 or code.status == 3 and \
                    (((datetime.datetime.now().replace(tzinfo=None) - code.end_dt.replace(tzinfo=None)).seconds) +
                (datetime.datetime.now().replace(tzinfo=None) - code.end_dt.replace(
                    tzinfo=None)).days * 24 * 3600) < seconds:
                code_id.append(code.id)
                id.append(f'{code.t_id}/{code.used_by_id}')
                create_dt.append(code.create_dt)
                end_dt.append(code.end_dt)
                if code.currency == 'btc':
                    type.append('BTC')
                    amount.append(f'{code.btc_value} BTC')
                else:
                    type.append('RUB')
                    amount.append(f'{code.rub_value} RUB')
                code_text.append(code.code)
                if code.status == 1:
                    status.append('Создан')
                elif code.status == 2:
                    status.append('Активирован')
                elif code.status == 3:
                    status.append('Отклонен')

    data = {
        'ID операции': code_id,
        'ID Создателя / id активировашего код': id,
        'Время операции': create_dt,
        'Время активации': end_dt,
        'Тип кода': type,
        'Количество': amount,
        'Код': code_text,
        'Статус': status
    }

    df = pd.DataFrame(data).sort_values(by='Время операции', ascending=True)
    if len(df['ID операции']) != 0:
        df['Время операции'] = df['Время операции'].dt.tz_localize(None)
        df['Время активации'] = df['Время активации'].dt.tz_localize(None)
    return df


def columns(writer):
    workbook= writer.book
    worksheet = writer.sheets['История кодов']

    worksheet.set_column('A:Z', width=18, cell_format=workbook.add_format({'align': 'center'}))
    worksheet.set_column('B:B', width=39)
    worksheet.set_column('C:C', width=20)




#print(pd.read_excel('../upload.xlsx'))