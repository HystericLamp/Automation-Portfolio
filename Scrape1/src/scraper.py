import requests
from bs4 import BeautifulSoup
import xlsxwriter

from .exceptions.failed_response_exception import FailedResponseException

class Scraper:
    def __init__(self, url):
        self.base_url = url
        self.books_data = []
        self.current_page = 1

    def connect_and_parse(self):
        while True:
            # make a GET request to url
            url = f"{self.base_url}page-{self.current_page}.html" if self.current_page > 1 else self.base_url
            response = requests.get(url)

            if response.status_code != 200:
                errMsg = """
                            Could not connect to server...\n
                            Server returned with error code 
                        """ + response.status_code
                
                raise FailedResponseException(errMsg)
            
            # Setup BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", class_="product_pod")

            # Parse a page
            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                self.books_data.append((title, price))

            print(f"Scraped page {self.page_number}")
            self.page_number += 1

            # Check if there is a "Next" button
            next_button = soup.find("li", class_="next")
            if next_button:
                self.current_page += 1  # Move to next page
            else:
                break  # Stop when there's no Next button

    def write_data_to_excel(self):
        workbook = xlsxwriter.Workbook('books_data.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        for title, price in self.books_data:
            worksheet.write(row, 0, title)
            worksheet.write(row, 1, price)
            row += 1

        workbook.close()