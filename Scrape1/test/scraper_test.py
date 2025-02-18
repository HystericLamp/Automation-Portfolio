import unittest
from unittest.mock import patch
import requests
from requests.models import Response
import os
import sys

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.scraper import Scraper
from src.exceptions.failed_response_exception import FailedResponseException

URL_TO_SCRAPE = "https://books.toscrape.com/"

class TestScraperMethods(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper(URL_TO_SCRAPE)

    @patch("src.scraper.requests.get")
    def test_connect_success(self, mock_get):
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"Fake response content"
        mock_get.return_value = mock_response

        response = self.scraper.connect(self.scraper.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Fake response content")

    @patch("src.scraper.requests.get")
    def test_connect_failure(self, mock_get):
        mock_response = Response()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(FailedResponseException) as context:
            self.scraper.connect(self.scraper.base_url)

        self.assertIn(
        "Could not connect to server... Server returned with error code 404",
        str(context.exception).replace("\n", "").strip()
)

    def test_categories(self):
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"""
            <div class="side_categories">
                <ul>
                    <li>
                        <ul>
                            <li><a href="/category/books/travel_2/index.html">Travel</a></li>
                            <li><a href="/category/books/crime_51/index.html">Crime</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        """

        categories, category_links = self.scraper.get_categories(mock_response)
        
        self.assertEqual(categories, ["Travel", "Crime"])
        self.assertEqual(category_links["Travel"], "https://books.toscrape.com/category/books/travel_2/index.html")
        self.assertEqual(category_links["Crime"], "https://books.toscrape.com/category/books/crime_51/index.html")

if __name__ == '__main__':
    unittest.main()