from datetime import datetime

import requests
import cryptocompare
from pycbrf.toolbox import ExchangeRates

TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'


def get_latest_crypto_price_usd(crypto):
    # cryptocompare.get_coin_list(format=False)
    return cryptocompare.get_historical_price_minute('BTC', 'USD', limit=1, exchange='binanceusa', toTs=datetime.now())


def get_latest_currency_price(currency):
    """
        ExchangeRate(
            id='R01235',
            name='Доллар США',
            code='USD',
            num='840',
            value=Decimal('65.5287'),
            par=Decimal('1'),
            rate=Decimal('65.5287'))
    """
    rates = ExchangeRates()
    return rates[currency]
