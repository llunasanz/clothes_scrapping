import re
import requests
from bs4 import BeautifulSoup
import argparse
import json


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


def split_currency_amount(s):
    currency = ''.join(filter(
        lambda char: not char.isdigit() and char != '.',
        s
    )).replace(" ", "")
    amount = float(''.join(filter(
        lambda char: char.isdigit() or char == '.',
        s
    )))
    return currency, amount

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
        if data:
            data_dict[class_to_key[class_name]] = data

    return json.dumps(data_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape product data from a URL.')
    parser.add_argument('url', type=str, help='The URL of the product page to scrape')

    args = parser.parse_args()

    product_data = scrape_product(args.url)
    print(product_data)
