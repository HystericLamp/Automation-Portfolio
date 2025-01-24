import subprocess
import platform
import os
import sys
from src.scraper import Scraper

"""
    Main function that updates requirements.txt with any new dependencies
    and runs the scraper
"""
URL_TO_SCRAPE = "https://books.toscrape.com/"

"""Update any new dependencies added"""
def update_requirements():
    # Check if a virtual environment is active
    if os.environ.get("VIRTUAL_ENV") is None:
        print("No virtual environment detected.")
        sys.exit(1)

    # Generate or update requirements.txt
    try:
        subprocess.run([sys.executable, "-m", "pip", "freeze", ">", "requirements.txt"], shell=True, check=True)
        print("requirements.txt updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

"""Activate the virtual environment and run the scraper."""
def activate_and_run():
    os_type = platform.system()

    # If OS is Windows
    if os_type == "Windows":
        activate_script = os.path.join(".venv", "Scripts", "activate")
    else:
        # If OS is Linux/Mac
        activate_script = os.path.join(".venv", "bin", "activate")

    # Command to activate the environment and run the scraper
    command = f"{activate_script}"
    subprocess.run(command, shell=True)
    
    scraper = Scraper(URL_TO_SCRAPE)
    scraper.connect_and_open()
    scraper.extract_contents()
    scraper.end_scrape()

if __name__ == "__main__":
    activate_and_run()
    update_requirements()
