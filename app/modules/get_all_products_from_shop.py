import sys
import os

# Ensure the root directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.modules.get_all_products_from_collection import get_all_product_details
from src.links_getter.get_all_collection_links import get_collection_from_shop

def get_all_products_recursively(collection_url="https://en.gb.scalperscompany.com/"):
    product_links = get_collection_from_shop(collection_url)
    all_product_details = []

    for product_url in product_links:
        details = get_all_product_details(product_url)
        all_product_details.extend(details)

    return all_product_details

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape all product details from a shop URL.")
    parser.add_argument(
        'url',
        type=str,
        nargs='?',
        default="https://en.gb.scalperscompany.com/",
        help='The shop URL to scrape'
    )
    
    args = parser.parse_args()
    collection_url = args.url

    all_details = get_all_products_recursively(collection_url)

    list(map(lambda details: print(details), product_details))
