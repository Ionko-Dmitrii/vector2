import requests

TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'


def get_latest_crypto_price(crypto):
    response = requests.get(TICKER_API_URL + crypto)
    response_json = response.json()

    return response_json[0]['price_usd']
