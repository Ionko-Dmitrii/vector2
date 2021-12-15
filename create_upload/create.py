import logging

from create_upload import exchange, transactions, codes, support, chat

log_file = '../upload.log'


import pandas as pd



def create_upload(minutes):
    try:
        writer = pd.ExcelWriter('./upload.xlsx', engine ='xlsxwriter')

        exchange.df(minutes * 60).to_excel(writer, sheet_name = 'Обмен', index=False)
        transactions.df(minutes * 60).to_excel(writer, sheet_name='История транзакций', index=False)
        codes.df(minutes * 60).to_excel(writer, sheet_name='История кодов', index=False)
        support.df(minutes * 60).to_excel(writer, sheet_name='Support', index=False)
        chat.df(minutes * 60).to_excel(writer, sheet_name='История действий', index=False)

        exchange.columns(writer)
        transactions.columns(writer)
        codes.columns(writer)
        support.columns(writer)
        chat.columns(writer)
        writer.save()
    except Exception as e:
        f = open(log_file, 'a')
        f.write(f'{e}')
        f.close()
        logging.exception(e)

