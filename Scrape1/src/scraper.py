import requests
from bs4 import BeautifulSoup
import xlsxwriter

from .exceptions.failed_response_exception import FailedResponseException

class Scraper:
    def __init__(self, url):
        self.base_url = url

    
    def connect(self, url):
        """Makes a connection to URL."""
        # make a GET request to url
        response = requests.get(url)

        if response.status_code != 200:
            errMsg = f"Could not connect to server... Server returned with error code {response.status_code}"
            
            raise FailedResponseException(errMsg)
        
        return response

    def get_genres(self, response):
        """Scrape and return all category links."""
        
        soup = BeautifulSoup(response.text, "html.parser")
        genres = []
        genre_links = {}
        
        # Find all category links
        web_links = soup.select(".side_categories ul li ul li a")
        
        for cat in web_links:
            genre_name = cat.text.strip()
            genre_url = self.base_url.rstrip("/") + "/" + cat["href"].lstrip("/")
            genres.append(genre_name)
            genre_links[genre_name] = genre_url
        
        return genres, genre_links

    def parse(self, genres, genre_links):
        """Scrape and returns book data"""
        books_data = []

        # Loop through all genres
        for genre in genres:
            current_page = 1
            response = self.connect(genre_links[genre])

            while True:
                # Parse a page
                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.find_all("article", class_="product_pod")

                for book in books:
                    title = book.h3.a["title"]
                    price = book.find("p", class_="price_color").text
                    books_data.append((title, price))

                print(f"Scraped page {current_page} of {genre}")

                # Check if there is a "Next" button
                next_button = soup.find("li", class_="next")
                if next_button:
                    current_page += 1
                else:
                    break  # Stop when there's no Next button
        


    def write_data_to_excel(self, books_data):
        """Writes all data into an excel file."""
        workbook = xlsxwriter.Workbook('books_data.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        for title, price in books_data:
            worksheet.write(row, 0, title)
            worksheet.write(row, 1, price)
            row += 1

        workbook.close()