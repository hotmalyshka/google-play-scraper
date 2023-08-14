import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging


# Class for scraping data from Google Play
class GooglePlayScraper:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.driver.quit()

    # Normalize URL to ensure it has a scheme
    @staticmethod
    def normalize_url(url):
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return "https://" + url
        else:
            return url

    # Scrape app data from the provided URL
    @staticmethod
    def scrape_app_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            # Log scraping activity
            logging.debug(f"Scraping data from URL: {url}")

            soup = BeautifulSoup(response.content, 'html.parser')

            name = soup.find('h1', {'itemprop': 'name'}).text.strip()
            age_rating = soup.find('span', {'itemprop': 'contentRating'}).text.strip()
            age_rating = age_rating.split()[-1]

            rating_text = soup.find('div', {'class': 'TT9eCd'}).text.strip()
            rating = float(re.search(r'\d+\.\d+', rating_text).group())

            reviews_text = soup.find('div', {'class': 'g1rdde'}).text.strip()
            reviews_text = reviews_text.replace(' reviews', '')
            if reviews_text.endswith('K'):
                reviews = float(reviews_text[:-1]) * 1000
            else:
                reviews = int(reviews_text)

            installs_element = soup.find_all('div', {'class': 'ClM7O'})
            installs = installs_element[1].text.strip()

            last_updated_str = soup.find('div', {'class': 'xg1aie'}).text.strip()
            format_str = "%b %d, %Y"
            last_updated = datetime.strptime(last_updated_str, format_str).date()

            review_ratings = [div['aria-label'] for div in soup.find_all('div', {'class': 'JzwBgb'})]
            for i in range(len(review_ratings)):
                review_ratings[i] = int(review_ratings[i].split()[0].replace(",", ""))

            return name, age_rating, rating, reviews, installs, last_updated, review_ratings
        else:
            return None

    # Get the version of the app using Selenium
    def get_version(self, url):
        self.driver.get(url)
        button = self.driver.find_element(By.XPATH,
                                          '//button[@class="VfPpkd-Bz112c-LgbsSe yHy1rc eT1oJ QDwDD mN1ivc VxpoF"]')
        button.click()

        main_window = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            if window_handle != main_window:
                self.driver.switch_to.window(window_handle)
                break

        time.sleep(2)

        data_element = self.driver.find_element(By.XPATH, '//div[@class="reAt0"]')
        data = data_element.text
        self.driver.switch_to.window(main_window)

        self.driver.quit()

        pattern = r'[^0-9.]'
        version = re.sub(pattern, '', data)

        return version