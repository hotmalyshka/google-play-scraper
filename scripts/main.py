import logging
from database_manager import DatabaseManager
from data_processor import DataProcessor
import config


def execute_data_collection():
    # Create an instance of the database manager and create necessary tables
    db_manager = DatabaseManager()
    db_manager.create_tables()

    # Read input data from a file
    input_data = []
    with open(config.INPUT_NAME, 'r') as file:
        next(file)  # Skip header line
        for line in file:
            domain, gplay_url = line.strip().split('\t')
            input_data.append({"domain": domain, 'gplay_url': gplay_url})

    # Create an instance of the data processor and collect/save data
    data_processor = DataProcessor(db_manager, input_data)
    data_processor.collect_and_save_data()


if __name__ == "__main__":
    # Setup logging configuration
    logging.basicConfig(filename=config.LOG_FILENAME, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    execute_data_collection()