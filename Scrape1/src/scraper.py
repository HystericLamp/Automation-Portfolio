import requests
from bs4 import BeautifulSoup
import xlsxwriter

from .exceptions.failed_response_exception import FailedResponseException

class Scraper:
    def __init__(self, url):
        self.url = url
        self.books_data = []
        self.page_number = 1

    def connect_and_parse(self):
        # make a GET request to url
        response = requests.get(self.url)

        if response.status_code != 200:
            errMsg = """
                        Could not connect to server...\n
                        Server returned with error code 
                    """ + response.status_code
            
            raise FailedResponseException(errMsg)
        
        # Parse the data
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            self.books_data.append((title, price))

        print(f"Scraped page {self.page_number}")
        self.page_number += 1

    def write_data_to_excel(self):
        workbook = xlsxwriter.Workbook('books_data.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        for col, data in enumerate(self.books_data):
            worksheet.write_column(row, col, data)

        workbook.close()
