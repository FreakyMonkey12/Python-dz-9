import aiohttp
import asyncio
import json
from datetime import datetime, timedelta


class PrivatBankAPI:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def fetch_data(self, date):
        async with aiohttp.ClientSession() as session:
            params = {
                'json': '',
                'date': date.strftime('%d.%m.%Y')
            }
            async with session.get(self.API_URL, params=params) as response:
                return await response.json()

    async def get_exchange_rate(self, currency, days):
        rates = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        while end_date >= start_date:
            data = await self.fetch_data(end_date)
            currency_data = next((item for item in data['exchangeRate'] if item['currency'] == currency), None)

            if currency_data:
                rate = {
                    end_date.strftime('%d.%m.%Y'): {
                        currency: {
                            'sale': currency_data['saleRate'],
                            'purchase': currency_data['purchaseRate']
                        }
                    }
                }
                rates.append(rate)

            end_date -= timedelta(days=1)

        return rates


async def main():
    api = PrivatBankAPI()

    try:
        eur_rates = await api.get_exchange_rate('EUR', 10)
        usd_rates = await api.get_exchange_rate('USD', 10)

        combined_rates = [{**eur, **usd} for eur, usd in zip(eur_rates, usd_rates)]

        print(json.dumps(combined_rates, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
