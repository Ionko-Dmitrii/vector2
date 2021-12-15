import pandas as pd

def upload_transactions(transactions):
    id = []
    create_dt = []
    got = []
    sent = []
    balance = []
    balance_was = []
    type = []
    commission = []
    info = []
    status = []
    end_dt = []
    answer = []
    to_address = []
    txid = []


    for transaction in transactions:
        id.append(transaction['id'])
        create_dt.append((transaction['dt']))
        got.append(transaction['got'])
        sent.append(transaction['sent'])
        balance.append(transaction['balance'])
        balance_was.append(transaction['balance_was'])
        type.append(transaction['type'])
        commission.append(transaction['commission'])
        info.append(transaction['info'])
        status.append(transaction['status'])
        end_dt.append(transaction['end_dt'])
        answer.append(transaction['answer'])
        to_address.append(transaction['to_address'])
        txid.append(transaction['txid'])

    data = {
        'ID': id,
        'Время транзакции': create_dt,
        'Получил': got,
        'Отправил': sent,
        'Баланс': balance,
        'Баланс был': balance_was,
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

    df['Время транзакции'] = df['Время транзакции'].dt.tz_localize(None)
    df['Время окончания'] = df['Время окончания'].dt.tz_localize(None)
    writer = pd.ExcelWriter('reference.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='История транзакций', index=False)
    workbook = writer.book
    worksheet = writer.sheets['История транзакций']
    worksheet.set_column('A:L', width=18, cell_format=workbook.add_format({'align': 'center'}))
    worksheet.set_column('A:A', width=20)
    worksheet.set_column('B:B', width=14)
    worksheet.set_column('C:C', width=14)
    worksheet.set_column('D:D', width=15)
    worksheet.set_column('E:F', width=15)
    worksheet.set_column('G:G', width=6)
    worksheet.set_column('H:L', width=18)
    writer.save()
    return len(transactions)


def upload_exchange(exchanges):
    id = []
    t_id = []
    create_dt = []
    type = []
    btc_value = []
    rub_value = []
    status = []
    commission = []
    currency_btc = []
    currency_usd = []
    end_dt = []
    admin_id = []
    for exchange in exchanges:
        id.append(exchange['id'])
        t_id.append(exchange['t_id'])
        create_dt.append(exchange['create_dt'])
        if exchange['type'] == 0:
            type.append('Продажа')
        elif exchange['type'] == 1:
            type.append('Покупка')
        btc_value.append(exchange['btc_value'])
        rub_value.append(exchange['rub_value'])
        if exchange['status'] == 0:
            status.append('Создается')
        elif exchange['status'] == 1:
            status.append('Создано')
        elif exchange['status'] == 2:
            status.append('Одобрено')
        elif exchange['status'] == 3:
            status.append('Отказано')
        commission.append(exchange['commission'])
        currency_btc.append(exchange['currency_btc'])
        currency_usd.append(exchange['currency_usd'])
        end_dt.append(exchange['end_dt'])
        admin_id.append(exchange['admin_id'])
    data = {
        'ID операции': id,
        'ID пользователя': t_id,
        'Время транзакции': create_dt,
        'Тип': type,
        'BTC': btc_value,
        'RUB': rub_value,
        'Статус': status,
        'Комиссия': commission,
        'Курс BTC': currency_btc,
        'Курс USD': currency_usd,
        'Время подтверждения': end_dt,
        'ID администратора': admin_id
    }

    df = pd.DataFrame(data).sort_values(by='Время транзакции', ascending=True)
    df['Время транзакции'] = df['Время транзакции'].dt.tz_localize(None)
    df['Время подтверждения'] = df['Время подтверждения'].dt.tz_localize(None)
    writer = pd.ExcelWriter('reference.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='История транзакций', index=False)
    workbook = writer.book
    worksheet = writer.sheets['История транзакций']

    worksheet.set_column('A:L', width=18, cell_format=workbook.add_format({'align': 'center'}))
    worksheet.set_column('A:A', width=5)
    writer.save()
    return len(exchanges)