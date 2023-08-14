import sqlite3
import config


# Class for managing the database
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE_NAME)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # Create necessary tables if they don't exist
    def create_tables(self):
        create_apps_table_query = '''
        CREATE TABLE IF NOT EXISTS apps(
            id INTEGER PRIMARY KEY,
            domain TEXT,
            name TEXT
        )
        '''
        create_app_history_table_query = '''
        CREATE TABLE IF NOT EXISTS app_history(
            id INTEGER PRIMARY KEY,
            app_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            domain TEXT,
            age_rating TEXT,
            rating REAL,
            reviews INTEGER,
            installs TEXT,
            last_updated DATE,
            version TEXT,
            review_5_star_count INTEGER,
            review_4_star_count INTEGER,
            review_3_star_count INTEGER,
            review_2_star_count INTEGER,
            review_1_star_count INTEGER,
            FOREIGN KEY (app_id) REFERENCES apps(id)
        )
        '''
        # Create the necessary tables
        self.cursor.execute(create_apps_table_query)
        self.cursor.execute(create_app_history_table_query)
        self.conn.commit()

    # Insert new app entry into the 'apps' table
    def insert_app(self, input_domain, name):
        self.cursor.execute("INSERT INTO apps (domain, name) VALUES (?, ?)", (input_domain, name))
        self.conn.commit()

    # Insert app data data into the 'app_history' table
    def insert_app_data(self, app_id, input_domain, age_rating, rating, reviews, installs, last_updated,
                        version, review_ratings):
        insert_query = '''
                INSERT INTO app_history (
                    app_id, domain, age_rating, rating, reviews, installs, last_updated, version, 
                    review_5_star_count, review_4_star_count, review_3_star_count, review_2_star_count, 
                    review_1_star_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
        self.cursor.execute(insert_query, (app_id, input_domain, age_rating, rating, reviews, installs,
                                           last_updated, version, review_ratings[0], review_ratings[1],
                                           review_ratings[2], review_ratings[3], review_ratings[4]))
        self.conn.commit()