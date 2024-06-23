import unittest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/test')))
import get_link_first_product

class TestGetFirstProductLink(unittest.TestCase):
    
    @patch('requests.get')
    def test_get_first_product_link(self, mock_get):
        # Mock the response for the main page
        mock_main_page_response = Mock()
        mock_main_page_response.status_code = 200
        mock_main_page_response.text = '''
        <html>
            <a href="/products/product1">Product 1</a>
            <a href="/products/product2">Product 2</a>
        </html>
        '''
        
        # Mock the response for the product page
        mock_product_page_response = Mock()
        mock_product_page_response.status_code = 200
        
        # Define the side effects of the mock_get function
        def side_effect(url, *args, **kwargs):
            if url == "https://en.gb.scalperscompany.com":
                return mock_main_page_response
            elif url.startswith("https://en.gb.scalperscompany.com/products/"):
                return mock_product_page_response
            return Mock(status_code=404)
        
        mock_get.side_effect = side_effect
        
        # Capture the output
        with patch('builtins.print') as mock_print:
            get_link_first_product.get_first_product_link()
            mock_print.assert_called_with("https://en.gb.scalperscompany.com/products/product1")

if __name__ == '__main__':
    unittest.main()

