import re
import requests
from bs4 import BeautifulSoup

url_to_shop = "https://en.gb.scalperscompany.com"

response = requests.get(url_to_shop)
soup = BeautifulSoup(response.text, 'html.parser')
a_href_list = list(map(lambda x: x.get("href"), soup.find_all("a")))
products_list = [href for href in a_href_list if href and href.startswith("/products")]

if products_list:
    print(url_to_shop + products_list[0])
else:
    print("No products found")
