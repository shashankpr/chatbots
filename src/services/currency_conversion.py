import requests
import logging
import api_settings

logging.basicConfig(level=logging.DEBUG)

access_key = api_settings.CURRENCY_LAYER_TOKEN


class CurrencyRates(object):
    def __init__(self):
        """
        Initialized Currency conversion call
        """
        self.base_url = "http://apilayer.net/api/"
        self.access_token = api_settings.CURRENCY_LAYER_TOKEN

    def _get_live_rate(self, destination_currency, path="live"):
        """
        Gets the current rate for destination currency in terms of USD
        :param destination_currency: 
        :param path: 
        :return: conversion rate in terms of USD
        """
        request_url = self.base_url + path
        payload = {'access_key': self.access_token, 'currencies': destination_currency, 'format': 1}

        resp = requests.get(request_url, params=payload)

        try:
            if resp.status_code == 200:
                # logging.info(resp.json())
                conversion_rate = resp.json()['quotes'].values()
                for currency_val in conversion_rate:
                    return float(currency_val)
        except:
            logging.debug("Could not identify the currency name")

    def get_conversion_rate(self, source, destination):
        """
        Gets conversion rate for a source different from USD
        :param source: 
        :param destination: 
        :return: currency rate in comparison with the source currency name
        """
        source_rate = self._get_live_rate(source)
        dest_rate = self._get_live_rate(destination)

        try:
            conversion_rate = dest_rate / source_rate
            logging.info(conversion_rate)
            return conversion_rate
        except:
            raise NameError("Invalid currency name")
            # logging.debug("Invalid currency name")


# c = CurrencyRates()
# c.get_conversion_rate('GBP', 'INR')
