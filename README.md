# Google Play Data Scraper

This project is a Python script for scraping data from Google Play Store for a list of apps and storing it in a SQLite database. It uses Selenium for handling dynamic content and BeautifulSoup for parsing HTML.

## Project Structure

The project is organized into several files and folders:

- `database/`: Contains the SQLite database file `app_data.db` where the scraped data is stored.
- `data/`: Contains the input file `input.txt` that lists the domains and Google Play URLs of the apps to scrape.
- `scripts/`: Contains the main scripts and modules of the project.
  - `config.py`: Configuration settings for the project, including database path, input file path, and log filename.
  - `scraper.py`: Contains the `GooglePlayScraper` class for scraping app data from Google Play.
  - `database_manager.py`: Contains the `DatabaseManager` class for managing the SQLite database.
  - `data_processor.py`: Contains the `DataProcessor` class for processing and saving scraped data.
  - `main.py`: The main script that orchestrates the data collection process.

To install the necessary dependencies, use the requirements.txt file, which contains a list of libraries and their versions.

## Installation and Usage

1. Clone the repository:

```sh
git clone https://github.com/hotmalyshka/google-play-scraper.git
cd google-play-scraper
```

2. Install the required dependencies:

```sh
pip install -r requirements.txt
```

3. Ensure you have the Chrome browser and the corresponding version of the ChromeDriver installed on your system for Selenium.

4. Update the `config.py` file with your desired configuration settings.

5. Prepare your input data by editing the `data/input.txt` file. Each line should have the format: `domain \t Google_Play_URL`.

6. Run the script:

```sh
python scripts/main.py
```

## Notes

- Make sure to respect website scraping policies and terms of use.
- The script might require adjustments depending on changes to the Google Play Store website layout.
- This project is for educational purposes and should be used responsibly.
