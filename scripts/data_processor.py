import sqlite3
import logging
from scraper import GooglePlayScraper
import config


# Class for processing data
class DataProcessor:
    def __init__(self, internal_db_manager, input_data_list):
        self.db_manager = internal_db_manager
        self.input_data = input_data_list

    # Collect and save data for each app in the input data list
    def collect_and_save_data(self):
        conn = sqlite3.connect(config.DATABASE_NAME)
        cursor = conn.cursor()

        for data in self.input_data:
            scraper = GooglePlayScraper()
            try:
                # Normalize the URL before processing
                normalized_url = scraper.normalize_url(data['gplay_url'])
                logging.debug(f"Processing domain: {data['domain']} with URL: {normalized_url}")

                # Scrape app data
                name, age_rating, rating, reviews, installs, last_updated, review_ratings = \
                    scraper.scrape_app_data(normalized_url)
                version = scraper.get_version(normalized_url)

                if name:
                    cursor.execute("SELECT id FROM apps WHERE domain = ?", (data['domain'],))
                    app_row = cursor.fetchone()

                    if app_row:
                        app_id = app_row[0]
                    else:
                        # Insert new app entry if not found
                        self.db_manager.insert_app(data['domain'], name)
                        app_id = cursor.lastrowid

                    # Insert app history data
                    self.db_manager.insert_app_data(app_id, data['domain'], age_rating, rating, reviews, installs,
                                                    last_updated, version, review_ratings)

                    conn.commit()
                    print("Data collected and saved.")
                    logging.debug("Data collected and saved.")
            except Exception as e:
                logging.error(f"An error occurred for domain {data['domain']}: {str(e)}")
            finally:
                # Clean up Selenium driver
                scraper.driver.quit()

        conn.close()