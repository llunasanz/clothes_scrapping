import unittest
from unittest.mock import patch, Mock
from src.scrapper import scrap
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

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

    @patch('src.scrapper.scrap.subprocess.run')
    def test_split_currency_amount(self, mock_subprocess_run):
        # Mock the return value of the subprocess.run call to simulate the bash script output
        mock_subprocess_run.return_value = Mock(stdout="0.85", returncode=0)
        
        test_cases = [
            ("£104", {
                'currency': 'GBP (£)', 
                'price_in_GBP': 104.0, 
                'price_in_EUR': 88.4,
                'price_in_CLP': 88.4,
                'price_in_COP': 88.4,
                'price_in_MXN': 88.4,
                'price_in_USD': 88.4, 
                'date_time_of_conversion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }),
            ("$99.99", {
                'currency': 'USD ($)', 
                'price_in_GBP': 84.99, 
                'price_in_EUR': 84.99,
                'price_in_CLP': 84.99,
                'price_in_COP': 84.99,
                'price_in_MXN': 84.99,
                'price_in_USD': 99.99, 
                'date_time_of_conversion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }),
            ("€1000", {
                'currency': 'EUR (€)', 
                'price_in_GBP': 850.0, 
                'price_in_EUR': 1000.0,
                'price_in_CLP': 850.0,
                'price_in_COP': 850.0,
                'price_in_MXN': 850.0,
                'price_in_USD': 850.0, 
                'date_time_of_conversion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }),
        ]
        
        for s, expected in test_cases:
            with self.subTest(s=s, url="http://test-url.com"):
                result = scrap.split_currency_amount(s,"http://test-url.com")
                # Check the dynamic date_time_of_conversion separately
                self.assertEqual(result['currency'], expected['currency'])
                self.assertAlmostEqual(result['price_in_GBP'], expected['price_in_GBP'], places=2)
                self.assertAlmostEqual(result['price_in_EUR'], expected['price_in_EUR'], places=2)
                self.assertAlmostEqual(result['price_in_USD'], expected['price_in_USD'], places=2)
                self.assertTrue('date_time_of_conversion' in result)
                self.assertIsNotNone(result['date_time_of_conversion'])

    @patch('src.scrapper.scrap.requests.get')
    @patch('src.scrapper.scrap.subprocess.run')
    def test_scrape_product(self, mock_subprocess_run, mock_get):
        # Mock the return value of the subprocess.run call to simulate the bash script output
        mock_subprocess_run.return_value = Mock(stdout="0.85", returncode=0)
        
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
            "currency": "GBP (£)",
            "price_in_EUR": 118.15,
            "price_in_GBP": 139.0,
            "price_in_USD": 118.15,
            "date_time_of_conversion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sizes": ["S", "M", "L"],
            "colours": ["BLACK"]
        }

        result = json.loads(scrap.scrape_product('http://test-url.com'))
        # Check the dynamic date_time_of_conversion separately
        self.assertEqual(result['product_url'], expected_data['product_url'])
        self.assertEqual(result['product_name'], expected_data['product_name'])
        self.assertEqual(result['sku'], expected_data['sku'])
        self.assertEqual(result['metadata'], expected_data['metadata'])
        self.assertEqual(result['images'], expected_data['images'])
        self.assertEqual(result['currency'], expected_data['currency'])
        self.assertAlmostEqual(result['price_in_GBP'], expected_data['price_in_GBP'], places=2)
        self.assertAlmostEqual(result['price_in_EUR'], expected_data['price_in_EUR'], places=2)
        self.assertAlmostEqual(result['price_in_USD'], expected_data['price_in_USD'], places=2)
        self.assertTrue('date_time_of_conversion' in result)
        self.assertIsNotNone(result['date_time_of_conversion'])
        self.assertEqual(result['sizes'], expected_data['sizes'])
        self.assertEqual(result['colours'], expected_data['colours'])

if __name__ == '__main__':
    unittest.main()
