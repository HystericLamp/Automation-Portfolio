from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def connect_and_open(self):
        # configure webdriver
        options = Options()
        options.headless = True  # hide GUI
        options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
        options.add_argument("start-maximized")  # ensure window is full-screen

        # configure chrome browser to not load images and javascript
        options.add_experimental_option(
            # this will disable image loading
            "prefs", {"profile.managed_default_content_settings.images": 2}
        )

        # Connect and open to URL
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)

        # wait for page to load
        element = WebDriverWait(driver=self.driver, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class]'))
        )

    def parse_contents(self):
        print(self.driver.page_source)

    def end_scrape(self):
        print("Closing driver...")
        self.driver.quit()