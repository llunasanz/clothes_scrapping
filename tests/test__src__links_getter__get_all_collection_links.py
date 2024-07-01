import unittest
from unittest.mock import patch, Mock
import sys
import os

# Import the function from src/links_getter/get_all_collection_links.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/links_getter')))
from get_all_collection_links import get_collection_from_shop

class TestGetCollectionFromShop(unittest.TestCase):

    @patch('requests.get')
    def test_get_collection_from_shop(self, mock_get):
        mock_main_page_response = Mock()
        mock_main_page_response.status_code = 200
        mock_main_page_response.text = '''
        <html>
            <a href="/collections/men-new-collection">Men's Collection</a>
            <a href="/collections/women-new-collection">Women's Collection</a>
            <a href="/collections/kids-new-collection">Kids' Collection</a>
        </html>
        '''

        mock_collection_response = Mock()
        mock_collection_response.status_code = 200

        def side_effect(url, *args, **kwargs):
            if url == "https://en.gb.scalperscompany.com":
                return mock_main_page_response
            elif url in [
                "https://en.gb.scalperscompany.com/collections/men-new-collection",
                "https://en.gb.scalperscompany.com/collections/women-new-collection",
                "https://en.gb.scalperscompany.com/collections/kids-new-collection"
            ]:
                return mock_collection_response
            return Mock(status_code=404)

        mock_get.side_effect = side_effect

        expected_urls = [
            "https://en.gb.scalperscompany.com/collections/men-new-collection",
            "https://en.gb.scalperscompany.com/collections/women-new-collection",
            "https://en.gb.scalperscompany.com/collections/kids-new-collection"
        ]

        result = get_collection_from_shop()
        self.assertEqual(result, sorted(expected_urls))

    @patch('requests.get')
    def test_get_collection_from_shop_with_custom_url(self, mock_get):
        custom_url = "http://custom-url.com"
        mock_main_page_response = Mock()
        mock_main_page_response.status_code = 200
        mock_main_page_response.text = '''
        <html>
            <a href="/collections/men-new-collection">Men's Collection</a>
            <a href="/collections/women-new-collection">Women's Collection</a>
        </html>
        '''

        mock_collection_response = Mock()
        mock_collection_response.status_code = 200

        def side_effect(url, *args, **kwargs):
            if url == custom_url:
                return mock_main_page_response
            elif url in [
                custom_url + "/collections/men-new-collection",
                custom_url + "/collections/women-new-collection"
            ]:
                return mock_collection_response
            return Mock(status_code=404)

        mock_get.side_effect = side_effect

        expected_urls = [
            custom_url + "/collections/men-new-collection",
            custom_url + "/collections/women-new-collection"
        ]

        result = get_collection_from_shop(custom_url)
        self.assertEqual(result, sorted(expected_urls))

    @patch('requests.get')
    def test_get_collection_from_shop_invalid_url(self, mock_get):
        mock_get.return_value = Mock(status_code=404)

        with self.assertRaises(ValueError) as context:
            get_collection_from_shop("http://invalid-url.com")

        self.assertIn("Failed to fetch the provided URL", str(context.exception))

    @patch('requests.get')
    def test_get_collection_from_shop_no_collections(self, mock_get):
        mock_main_page_response = Mock()
        mock_main_page_response.status_code = 200
        mock_main_page_response.text = '''
        <html>
            <a href="/about">About Us</a>
            <a href="/contact">Contact</a>
        </html>
        '''

        mock_get.return_value = mock_main_page_response

        result = get_collection_from_shop()
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
