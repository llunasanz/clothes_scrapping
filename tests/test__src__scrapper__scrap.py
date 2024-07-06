import unittest
from unittest.mock import patch, Mock
from src.scrapper import scrap
from bs4 import BeautifulSoup
import os
import json

class TestScrap(unittest.TestCase):

    def setUp(self):
        # Path to the HTML file
        file_path = os.path.join(os.path.dirname(__file__), 'assets', 'example_skirt_000.html')
        
        # Read the HTML file content
        with open(file_path, 'r') as file:
            self.sample_html = file.read()

        self.soup = BeautifulSoup(self.sample_html, 'html.parser')

    def test_extract_data_title(self):
        result = scrap.extract_data(self.soup, 'ProductMeta__Title')
        self.assertEqual(result, 'NEW LEATHER BELT SKIRT')

    def test_extract_data_sku(self):
        result = scrap.extract_data(self.soup, 'ProductMeta__SkuNumber')
        self.assertEqual(result, '8445279529418')

    def test_extract_data_description(self):
        result = scrap.extract_data(self.soup, 'ProductMeta__Description')
        self.assertEqual(result, 'NEW LEATHER BELT SKIRT')

    def test_extract_data_images(self):
        result = scrap.extract_data(self.soup, 'img')
        self.assertEqual(result, [
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-1_b11c05e2-f100-4d5d-aba3-cee484bbbb1e.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-2_468e4a50-103a-472d-ad10-e3613022461c.jpg?v=1715949821',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-3_708adc76-67a9-492d-9198-be6964dba90e.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-4.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-1.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-2.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-1_b11c05e2-f100-4d5d-aba3-cee484bbbb1e_250x.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-1_b11c05e2-f100-4d5d-aba3-cee484bbbb1e_800x.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-2_468e4a50-103a-472d-ad10-e3613022461c_800x.jpg?v=1715949821',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-3_708adc76-67a9-492d-9198-be6964dba90e_800x.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-4_800x.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-1_800x.jpg?v=1715949820',
            'https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-2_800x.jpg?v=1715949820'
        ])

    def test_extract_data_price(self):
        result = scrap.extract_data(self.soup, 'ProductMeta__Price')
        self.assertEqual(result, '£139')

    def test_extract_data_sizes(self):
        result = scrap.extract_data(self.soup, 'sizes')
        self.assertEqual(result, ['S', 'M', 'L'])

    def test_extract_data_colours(self):
        result = scrap.extract_data(self.soup, 'colours')
        self.assertEqual(result, ['BLACK'])

    def test_split_currency_amount(self):
        test_cases = [
            ("£104", ("£", 104.0)),
            ("$99.99", ("$", 99.99)),
            ("€1000", ("€", 1000.0)),
            ("1000€", ("€", 1000.0)),
            ("1000 lei", ("lei", 1000.0)),
            ("¥5000", ("¥", 5000.0)),
            ("₹75", ("₹", 75.0))
        ]
        for s, expected in test_cases:
            with self.subTest(s=s):
                result = scrap.split_currency_amount(s)
                self.assertEqual(result, expected)

    @patch('src.scrapper.scrap.requests.get')
    def test_scrape_product(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        mock_get.return_value = mock_response

        expected_data = {
            "product_url": "http://test-url.com",
            "product_name": "NEW LEATHER BELT SKIRT",
            "sku": "8445279529418",
            "metadata": "NEW LEATHER BELT SKIRT",
            "images": [
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-1_b11c05e2-f100-4d5d-aba3-cee484bbbb1e.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-2_468e4a50-103a-472d-ad10-e3613022461c.jpg?v=1715949821",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-3_708adc76-67a9-492d-9198-be6964dba90e.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-4.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-1.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-2.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-1_b11c05e2-f100-4d5d-aba3-cee484bbbb1e_250x.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-1_b11c05e2-f100-4d5d-aba3-cee484bbbb1e_800x.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-2_468e4a50-103a-472d-ad10-e3613022461c_800x.jpg?v=1715949821",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-3_708adc76-67a9-492d-9198-be6964dba90e_800x.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-P-4_800x.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-1_800x.jpg?v=1715949820",
                "https://en.gb.scalperscompany.com/cdn/shop/files/34764-BLACK-S-2_800x.jpg?v=1715949820"
            ],
            "price": "£139",
            "sizes": ["S", "M", "L"],
            "colours": ["BLACK"]
        }

        result = json.loads(scrap.scrape_product('http://test-url.com'))
        self.assertEqual(result, expected_data)

if __name__ == '__main__':
    unittest.main()
