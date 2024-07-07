import re
import requests
from bs4 import BeautifulSoup
import argparse
import json
import subprocess
from datetime import datetime


class_to_tag = {
    'ProductMeta__Title': 'h1',
    'ProductMeta__SkuNumber': 'span',
    'ProductMeta__Description': 'div',
    'img': 'img',
    'ProductMeta__Price': 'span',
    'sizes': 'option',
    'colours': 'option'
}


class_to_key = {
    'ProductMeta__Title': 'product_name',
    'ProductMeta__SkuNumber': 'sku',
    'ProductMeta__Description': 'metadata',
    'img': 'images',
    'ProductMeta__Price': 'price',
    'sizes': 'sizes',
    'colours': 'colours'
}

google_finance_url = "https://www.google.com/finance/quote/"


def symbol_to_code(symbol):
    # Dictionary mapping currency symbols to their respective codes
    currency_map = {
        "€": "EUR",   # Euro
        "$": "USD",   # US Dollar
        "£": "GBP",   # British Pound
        "¥": "JPY",   # Japanese Yen
        "₹": "INR",   # Indian Rupee
        "CHF": "CHF", # Swiss Franc
        "₩": "KRW",   # South Korean Won
        "C$": "CAD",  # Canadian Dollar
        "A$": "AUD",  # Australian Dollar
        "NZ$": "NZD", # New Zealand Dollar
        "HK$": "HKD", # Hong Kong Dollar
        "kr": "SEK",  # Swedish Krona
        "R$": "BRL",  # Brazilian Real
        "₽": "RUB",   # Russian Ruble
        "₪": "ILS",   # Israeli Shekel
        "₫": "VND",   # Vietnamese Dong
        "₺": "TRY",   # Turkish Lira
        "lei": "RON", # Romanian Leu
        "₦": "NGN",   # Nigerian Naira
        "฿": "THB",   # Thai Baht
        "₵": "GHS",   # Ghanaian Cedi
        "₭": "LAK",   # Lao Kip
        "MK": "MWK",  # Malawian Kwacha
        "P": "PHP"    # Philippine Peso
    }
    
    # Look up the currency code in the dictionary, default to the original symbol if not found
    return currency_map.get(symbol, symbol)


def get_last_price(url):
    # Define the path to the bash script
    script_path = './infra/get_last_price.sh'
    
    # Call the bash script with the provided URL
    result = subprocess.run(['bash', script_path, url], capture_output=True, text=True)
    
    # Check if the script execution was successful
    if result.returncode != 0:
        print("Error occurred:")
        print(result.stderr)
        return None
    
    # Convert the output to float
    try:
        price = float(result.stdout.strip())
    except ValueError:
        print("Failed to convert the output to float")
        return None

    return price


def split_currency_amount(s):
    currency = ''.join(filter(
        lambda char: not char.isdigit() and char != '.',
        s
    )).replace(" ", "")
    code_currency = symbol_to_code(currency)
    amount = float(''.join(filter(
        lambda char: char.isdigit() or char == '.',
        s
    )))
    
    # Define the currencies you want to convert to
    target_currencies = ["EUR", "GBP", "USD"]
    
    # Initialize the currency dictionary
    currency_dict = {
        'currency': code_currency + " (" + currency + ")",
        'date_time_of_conversion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Function to add price to the dictionary
    add_price = lambda target_currency: (
        f"price_in_{target_currency}", 
        round(amount, 2) if code_currency == target_currency else round(amount * get_last_price(google_finance_url + code_currency + "-" + target_currency), 2)
    )
    
    # Use map and lambda to iterate over target currencies and update the dictionary
    currency_dict.update(dict(map(add_price, target_currencies)))
    return currency_dict

size_order = ["XXXS", "XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]
size_index = dict(map(lambda x: (x[1], x[0]), enumerate(size_order)))
size_pattern = re.compile(r'\b(?:XXXS|XXS|XS|S|M|L|XL|XXL|XXXL)\b')


def sort_sizes(sizes):
    # Sort sizes based on their position in the predefined order
    size_index = size_index = dict(map(
        lambda x: (x[1], x[0]),
        enumerate(size_order)
    ))
    return sorted(
        sizes, key=lambda size: size_index.get(size, len(size_order))
    )


def extract_images(soup):
    list_items = soup.find_all('img')
    product_name = soup.find('h1', class_='ProductMeta__Title').text.strip()
    matching_images_0 = list(filter(None, map(
        lambda x: x.get('data-original-src')
            if x.get('alt') == product_name
            else '', 
        list_items
    )))
    matching_images_1 = list(filter(None, map(
        lambda x: x.get('src')
            if x.get('alt') == product_name
            else '', 
        list_items
    )))
    matching_images = matching_images_0 + matching_images_1
    return list(map(lambda x: 'https:' + x, matching_images))


def extract_sizes(soup):
    options = soup.find_all('option')
    sizes = filter(None, map(
        lambda x: size_pattern.search(x.text.strip()).group(0)
            if size_pattern.search(x.text.strip())
            else '',
            options
        ))
    return sort_sizes(list(set(sizes)))


def extract_colours(soup):
    options = soup.find_all('option')
    colours = filter(None, map(
        lambda x: x.text.split(' - ')[0].strip().split('/')[0].strip()
            if size_pattern.search(x.text.strip())
            else '',
            options
        ))
    return list(set(colours))


def extract_list_items(element):
    return list(map(
        lambda item: item.get_text(strip=True),
        element.find_all('li')
    ))


def extract_data(soup, class_name):
    # Get the tag name from the dictionary
    tag_name = class_to_tag.get(class_name)

    # Take care about special cases (images, sizes and colours)
    special_cases = {
        'img': lambda: extract_images(soup),
        'sizes': lambda: extract_sizes(soup),
        'colours': lambda: extract_colours(soup)
    }
    
    if class_name in special_cases:
        return special_cases[class_name]()

    # Find the element with the given class name and tag
    element = soup.find(tag_name, class_=class_name)

    # Check if there are any <li> tags within the element
    if element:
        try:
            list_items = extract_list_items(element)
            return list_items if list_items else element.get_text(strip=True)
        except Exception:
            return element.get_text(strip=True)
    return ""


def scrape_product(url):
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful and initialize BeautifulSoup object
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    data_dict = {"product_url": url}

    # Using more specific CSS selectors to target the div correctly
    details_div = soup.select_one('.Collapsible.Collapsible--large .Collapsible__Content')

    # Iterate over class_to_tag keys directly
    for class_name in class_to_tag:
        data = extract_data(soup, class_name)
        # Extract price conversion
        if data and class_name == "ProductMeta__Price":
            update_data_dict = lambda d, u: d.update(u)
            data_dict_prices = split_currency_amount(data)
            for key, value in data_dict_prices.items():
                update_data_dict(data_dict, {key: value})
            continue
        # Other data classes
        if data:
            data_dict[class_to_key[class_name]] = data

    return json.dumps(data_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape product data from a URL.')
    parser.add_argument('url', type=str, help='The URL of the product page to scrape')

    args = parser.parse_args()

    product_data = scrape_product(args.url)
    print(product_data)
