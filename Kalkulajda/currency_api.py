"""
@file currency_converter.py
@brief File containing Api for currency conversion.

@author Martin Valapka (xvalapm00)
@date 01.10. 2024
"""

import requests

API_URL = "https://api.exchangerate-api.com/v4/latest/euro"


def get_supported_currencies():
    url = f"{API_URL}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('rates', {}).keys()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def get_exchange_rate(base_currency, target_currency):
    url = f"{API_URL}{base_currency.upper()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rates = data.get('rates', {})
        return rates.get(target_currency.upper(), None)
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
