from typing import List
import asyncio
import aiohttp

from fake_useragent import UserAgent


class GetDataGoldCrown:
    _url_all_send_countries = 'https://koronapay.com/transfers/online/api/transfers/directions/points/receiving?'
    _params_all_send_countries = {'receivingMethod': 'cash'}
    _url_receiving_currency = 'https://koronapay.com/transfers/online/api/transfers/tariffs/info?'
    _params_receiving_currency = {
        'paymentMethod':'debitCard',
        'forTransferRepeat': 'false'}
    _url_get_price = 'https://koronapay.com/transfers/online/api/transfers/tariffs?'
    _params_get_price = {
        'paymentMethod':'debitCard',
        'receivingAmount':'10000',
        'receivingMethod':'cash',
        'paidNotificationEnabled':'false'}


    def __init__(self):
        self.headers = {"user-agent": UserAgent().random}

    async def get_price(self,
        receiving_country,
        receiving_currency,
        sending_country='RUS',
        sending_currency='810') -> float:
        try:
            params = self._params_get_price
            params['sendingCountryId'] = sending_country
            params['sendingCurrencyId'] = sending_currency
            params['receivingCountryId'] = receiving_country
            params['receivingCurrencyId'] = receiving_currency
            json = await self._get_json(
                url=self._url_get_price,
                params=params
            )
            if not json:
                return float(0)
            return float(json[0]['exchangeRate'])
        except KeyError as e:
            print(f'get_price \n{e}\n{receiving_country=}\n{receiving_currency=}')

    async def get_all_send_countries(self,
        country='RUS') -> List[tuple]:
        params = self._params_all_send_countries
        params['sendingCountryId'] = country
        json = await self._get_json(
            url=self._url_all_send_countries,
            params=params
        )
        if not json:
            return []
        return [(el['country']['id'], el['country']['name'])
                for el in json
                if el.get('country')]


    async def get_receiving_currency(
        self,
        receiving_country,
        sending_country='RUS') -> List[tuple]:

        params = self._params_receiving_currency
        params['sendingCountryId'] = sending_country
        params['receivingCountryId'] = receiving_country
        json = await self._get_json(
            url=self._url_receiving_currency,
            params=params
        )
        if not json:
            return []

        return [(el['receivingCurrency']['id'],
                 el['receivingCurrency']['code'],
                 el['receivingCurrency']['name'])
                for el in json
                if el['receivingCurrency']['code'] != 'RUB']

    




    async def _get_json(self, url, params=None, method='GET'):
        if not params: params = {}

        async with aiohttp.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params) as resp:
            if resp.status != 200:
                print(f'Статус {resp.status}\n{url}\n{params}')
                return {}
            json = await resp.json(content_type=None)
            if not json:
                print(f'Пустой JSON\n{url}')
            return json
