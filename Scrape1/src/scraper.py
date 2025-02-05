import requests
from bs4 import BeautifulSoup
import time

from exceptions.failed_response_exception import FailedResponseException

class Scraper:
    def __init__(self, url):
        self.url = url

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