from datetime import datetime

import cryptocompare
from pycbrf.toolbox import ExchangeRates


def get_latest_crypto_price_usd(crypto):
    return cryptocompare.get_historical_price_minute('BTC', 'USD', limit=1, exchange='binanceusa', toTs=datetime.now())


def get_latest_currency_price(currency):

    rates = ExchangeRates()
    return rates[currency]
