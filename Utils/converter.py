import requests


class Converter:
    def __init__(self, source: str, destination: str):
        self.source = source
        self.destination = destination

    def get_all_exchange_rates(self):
        exchange_rates = 0
        url = f"https://open.er-api.com/v6/latest/{self.source}"
        data = requests.get(url).json()

        if data["result"] == "success":
            exchange_rates = data["rates"]

        return exchange_rates

    def convert(self, amount: int) -> int:
        exchange_rates = self.get_all_exchange_rates()
        return int(exchange_rates[self.destination] * int(amount))


#  USAGE:

"""

converter = Converter("USD", "RUB")
dollars = 12
rubs = converter.convert(dollars)
print(rubs)

"""
