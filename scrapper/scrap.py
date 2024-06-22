import re
import requests
from bs4 import BeautifulSoup
import argparse

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

def extract_data(soup, class_name):
    # Get the tag name from the dictionary
    tag_name = class_to_tag.get(class_name)

    # Take care about special cases (images, sizes and colours)
    if tag_name == 'img':
        list_items = soup.find_all('img')
        product_name = soup.find('h1', class_='ProductMeta__Title').text.strip()
        matching_images_0 = list(filter(None, map(
            lambda x: x.get('data-original-src') if x.get('alt') == product_name else '', 
            list_items
        )))
        matching_images_1 = list(filter(None, map(
            lambda x: x.get('src') if x.get('alt') == product_name else '', 
            list_items
        )))
        matching_images = matching_images_0 + matching_images_1
        matching_images = list(map(lambda x: 'https:' + x, matching_images))
        return matching_images

    size_pattern = re.compile(r'\b(?:XXXS|XXS|XS|S|M|L|XL|XXL|XXXL)\b')

    if class_name == 'sizes':
        sizes = list(filter(None, map(
            lambda x: size_pattern.search(x.text.strip()).group(0) if size_pattern.search(x.text.strip()) else '', 
            soup.find_all('option')
        )))
        return list(set(sizes))

    if class_name == 'colours':
        colours = list(filter(None, map(
            lambda x: x.text.split(' - ')[0].strip().split('/')[0].strip() if size_pattern.search(x.text.strip()) else '', 
            soup.find_all('option')
        )))
        return list(set(colours))    

    # Find the element with the given class name and tag
    element = soup.find(tag_name, class_=class_name)

    # Check if there are any <li> tags within the element
    list_items = element.find_all('li')
    if list_items:
        # Extract the text from each <li> tag
        return [item.get_text(strip=True) for item in list_items]
    
    # Extract the text content of the element
    return element.get_text(strip=True)

def scrape_product(url):
    data_dict = {}
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return {}

    # Using more specific CSS selectors to target the div correctly
    details_div = soup.select_one('.Collapsible.Collapsible--large .Collapsible__Content')

    class_names = list(class_to_tag.keys())

    data_dict["product_url"] = url

    for class_name in class_names:
        data = extract_data(soup, class_name)
        if data:
            # Map the class name to the final dictionary key
            dict_key = class_to_key[class_name]
            data_dict[dict_key] = data

    return data_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape product data from a URL.')
    parser.add_argument('url', type=str, help='The URL of the product page to scrape')

    args = parser.parse_args()

    product_data = scrape_product(args.url)
    print(product_data)
