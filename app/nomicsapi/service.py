# pragma: no cover
import asyncio
import httpx
import json

API_KEY = 'ca109ae5159d18fc47942615b0f5018a29869a17'

class NomicsAPIHandler:
    def __init__(self):
        self._base_url = f'https://api.nomics.com/v1/currencies/ticker?key={API_KEY}'

    async def get_asset_data(self, *ids):
        async with httpx.AsyncClient() as client:
            req_url = self._base_url + '&ids=' + ','.join(ids)
            res = await client.get(req_url)

        res_data = res.json()
        return {
            asset_data['id']: {'price': asset_data['price'], 'logo_url': asset_data['logo_url']}
            for asset_data in res_data
        }


api_handler = NomicsAPIHandler()
