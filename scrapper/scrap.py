import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # URL of the webpage to scrape
    url = 'https://en.gb.scalperscompany.com/products/bbcstudio24-50505-strapless-linen-dress-ss24-red'
    data_dict = {}
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

    # Using more specific CSS selectors to target the div correctly
    details_div = soup.select_one('.Collapsible.Collapsible--large .Collapsible__Content')

    # Extracting the product name
    product_name = soup.find('h1', class_='ProductMeta__Title')
    if product_name:
        data_dict['product_name'] = product_name.text.strip()

    # Print the product details dictionary
    print(data_dict)
