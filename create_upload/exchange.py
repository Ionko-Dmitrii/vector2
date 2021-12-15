import xlsxwriter
import datetime
import pandas as pd
from openpyxl import load_workbook
from decimal import Decimal

import dbworker

exchanges = dbworker.get_all_exchange()


def df(seconds):
    id_operation = []
    t_id = []
    create_dt = []
    type = []
    X = []
    commission = []
    X_without_comm = []
    currency_formula = []
    currency_sum = []

    end_dt = []
    admin_id = []

    if exchanges != 0:
        for exchange in exchanges:

            if (((datetime.datetime.now().replace(tzinfo=None) - exchange.end_dt.replace(tzinfo=None)).seconds) +
                (datetime.datetime.now().replace(tzinfo=None) - exchange.end_dt.replace(
                    tzinfo=None)).days * 24 * 3600) < seconds\
                    and exchange.status == 2:
                id_operation.append(exchange.id)
                t_id.append(exchange.t_id)
                create_dt.append(exchange.create_dt)
                if exchange.type == 0:
                    type.append('ПРОДАЖА')
                    X.append(f'{exchange.btc_value:.8f} BTC')
                    commission.append(f'{exchange.commission:.8f} BTC')
                    X_without_comm.append(f'{(exchange.btc_value - exchange.commission):.8f} BTC')



                elif exchange.type == 1:
                    type.append('ПОКУПКА')
                    X.append(f'{exchange.rub_value:.2f} RUB')
                    commission.append(f'{exchange.commission:.2f} RUB')
                    X_without_comm.append(f'{(exchange.rub_value - exchange.commission):.2f} RUB')

                else:
                    type.append('НЕОПРЕДЕЛЕН')
                    X.append(' ')
                    commission.append(' ')
                    X_without_comm.append(' ')
                    currency_formula.append(' ')
                currency_formula.append(
                    f'{exchange.currency_btc}*{exchange.currency_usd}')
                currency_sum.append(f'{(exchange.currency_btc * exchange.currency_usd):.2f}₽')
                end_dt.append(exchange.end_dt)
                admin_id.append(exchange.admin_id)

    df = pd.DataFrame({
        'ID операции': id_operation,
        'ID пользователя': t_id,
        'Время создания операции': create_dt,
        'Направление операции': type,
        'Количество': X,
        'Комиссия': commission,
        'Без комиссии': X_without_comm,
        'Курс-формула': currency_formula,
        'Курс-сумма': currency_sum,
        'Завершение операции': end_dt,
        'ID администратора': admin_id
    })

    if len(df['ID операции']) != 0:
        df['Время создания операции'] = df['Время создания операции'].dt.tz_localize(None)
        df['Завершение операции'] = df['Завершение операции'].dt.tz_localize(None)
    return df


def columns(writer):
    workbook= writer.book

    worksheet = writer.sheets['Обмен']

    worksheet.set_column('A:Z', width=17, cell_format=workbook.add_format({'align': 'center'}))
    worksheet.set_column('D:D', 22)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('H:H', 20)
    worksheet.set_column('I:I', 17)
    worksheet.set_column('K:K', 23)
    worksheet.set_column('J:J', 20)


'''
writer = pd.ExcelWriter('upload.xlsx', engine ='xlsxwriter')
df(24 * 3600).to_excel(writer, sheet_name='Обмен', index=False)
columns(writer)
writer.save()
'''
#print(pd.read_excel('upload.xlsx'))