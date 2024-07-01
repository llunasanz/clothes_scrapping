import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the app/modules directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/modules')))

from get_all_products_from_collection import get_all_product_details

class TestGetAllProductDetails(unittest.TestCase):

    @patch('get_all_products_from_collection.get_product_links_from_page')
    @patch('get_all_products_from_collection.scrape_product')
    def test_get_all_product_details(self, mock_scrape_product, mock_get_product_links_from_page):
        # Mock data
        mock_collection_url = "https://en.gb.scalperscompany.com/collections/women-new-collection"
        mock_product_links = [
            "https://en.gb.scalperscompany.com/products/12345-product-one",
            "https://en.gb.scalperscompany.com/products/67890-product-two"
        ]
        mock_product_details = [
            {
                'product_url': "https://en.gb.scalperscompany.com/products/12345-product-one",
                'product_name': "Product One",
                'sku': '12345',
                'metadata': ['Feature 1', 'Feature 2'],
                'images': ['https://image1.jpg', 'https://image2.jpg'],
                'price': '£50',
                'sizes': ['S', 'M', 'L'],
                'colours': ['Red', 'Blue']
            },
            {
                'product_url': "https://en.gb.scalperscompany.com/products/67890-product-two",
                'product_name': "Product Two",
                'sku': '67890',
                'metadata': ['Feature A', 'Feature B'],
                'images': ['https://image3.jpg', 'https://image4.jpg'],
                'price': '£70',
                'sizes': ['M', 'L', 'XL'],
                'colours': ['Green', 'Yellow']
            }
        ]

        # Set up the mocks
        mock_get_product_links_from_page.return_value = mock_product_links
        mock_scrape_product.side_effect = mock_product_details

        # Expected result
        expected_result = [
            {
                'product_url': "https://en.gb.scalperscompany.com/products/12345-product-one",
                'product_name': "Product One",
                'sku': '12345',
                'metadata': ['Feature 1', 'Feature 2'],
                'images': ['https://image1.jpg', 'https://image2.jpg'],
                'price': '£50',
                'sizes': ['S', 'M', 'L'],
                'colours': ['Red', 'Blue'],
                'collection_url': mock_collection_url
            },
            {
                'product_url': "https://en.gb.scalperscompany.com/products/67890-product-two",
                'product_name': "Product Two",
                'sku': '67890',
                'metadata': ['Feature A', 'Feature B'],
                'images': ['https://image3.jpg', 'https://image4.jpg'],
                'price': '£70',
                'sizes': ['M', 'L', 'XL'],
                'colours': ['Green', 'Yellow'],
                'collection_url': mock_collection_url
            }
        ]

        # Run the function
        result = get_all_product_details(mock_collection_url)

        # Assert the result
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

