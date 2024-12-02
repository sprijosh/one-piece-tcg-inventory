import bs4
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


def setup_driver():
    """Set up the Selenium WebDriver."""
    chrome_options = Options()
    service = Service("./msedgedriver.exe")
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Edge(service=service, options=chrome_options)
    return driver

setup_driver()

def main(baseURL):
    driver = setup_driver()
    driver.get(baseURL)

    """Click different set filter to get the card list"""
    

    html = bs4.BeautifulSoup(driver.page_source, 'lxml')




if __name__ == "__main__":
    main("https://asia-hk.onepiece-cardgame.com/cardlist")