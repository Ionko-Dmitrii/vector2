import xlsxwriter
import datetime
import pandas as pd
from openpyxl import load_workbook
from decimal import Decimal

import dbworker
transactions = dbworker.get_all_transactions()


def df(seconds):
    create_dt = []
    got = []
    sent = []
    balance_was = []
    balance = []
    type = []
    commission = []
    info = []
    status = []
    end_dt = []
    answer = []
    to_address = []
    txid = []

    for transaction in transactions:
        if (((datetime.datetime.now().replace(tzinfo=None) - transaction.end_dt.replace(tzinfo=None)).seconds) +
            (datetime.datetime.now().replace(tzinfo=None) - transaction.end_dt.replace(
                tzinfo=None)).days * 24 * 3600) < seconds:
            create_dt.append(transaction.dt)
            got.append(transaction.got)
            sent.append(transaction.sent)
            balance_was.append(transaction.balance_was)
            balance.append(transaction.balance)
            type.append(transaction.type)
            commission.append(transaction.commission)
            info.append(transaction.info)
            status.append(transaction.status)
            end_dt.append(transaction.end_dt)
            answer.append(transaction.answer)
            to_address.append(transaction.to_address)
            txid.append(transaction.txid)

        data = {
            'Время транзакции': create_dt,
            'Получил': got,
            'Отправил': sent,
            'Баланс был': balance_was,
            'Баланс': balance,
            'Тип': type,
            'Комиссия': commission,
            'Описание\инфо': info,
            'Статус': status,
            'Время окончания': end_dt,
            'Причина отказа': answer,
            'На адрес': to_address,
            'Txid': txid
        }

    df = pd.DataFrame(data).sort_values(by='Время транзакции', ascending=True)
    if len(df['Время транзакции']) != 0:
        df['Время транзакции'] = df['Время транзакции'].dt.tz_localize(None)
        df['Время окончания'] = df['Время окончания'].dt.tz_localize(None)
    return df

def columns(writer):
    workbook= writer.book
    worksheet = writer.sheets['История транзакций']

    worksheet.set_column('A:L', width=18, cell_format=workbook.add_format({'align': 'center'}))
    worksheet.set_column('A:A', width=20)
    worksheet.set_column('B:B', width=14)
    worksheet.set_column('C:C', width=14)
    worksheet.set_column('D:D', width=15)
    worksheet.set_column('E:E', width=15)
    worksheet.set_column('G:G', width=20)
    worksheet.set_column('H:L', width=18)

#writer = pd.ExcelWriter('upload.xlsx', engine='xlsxwriter')
#df(24 * 3600).to_excel(writer, sheet_name='История транзакций', index=False)
#columns(writer)
#writer.save()