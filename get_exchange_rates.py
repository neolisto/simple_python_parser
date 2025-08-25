import requests
from bs4 import BeautifulSoup

source_page = "https://www.conti.waw.pl/"
response = requests.get(source_page)
list_of_currencies  = ["USD", "EUR", "GBP", "CHF", "JPY"]
currency_array = {}

def fetch_currency_strings(currency_short):
    """
    This function parses the HTML content of the given webpage and extracts currency information
    for the specified currency short code (e.g., 'USD', 'EUR').
    """
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all elements containing mentioned in currency
        currency_field = soup.find_all(lambda tag: tag.name == "option" and currency_short in tag.text)
        currency_list = list(currency_field)
        return currency_list
    else:
        print("Failed to fetch data from the web.")

for currency_short in list_of_currencies:
    currency = fetch_currency_strings(currency_short)
    exchange_rates = ["", ""]
    item_index = 0

    is_it_buy = True

    for rate in currency:
        # Extract number from the value attribute
        price = rate.get('value')
        if is_it_buy:
            exchange_rates[0] = f"{float(price)}"
            is_it_buy = False
        else:
            exchange_rates[1] = f"{float(price)}"

    currency_array[currency_short] = f'{exchange_rates[0]} / {exchange_rates[1]}'

print(f"{currency_array}")
