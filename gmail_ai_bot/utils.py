import os
import csv
import logging

from .config import TRAINING_DATA_PATH, LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def initialize_training_data():
    """
    Initialize the training data CSV file if it doesn't exist.

    Creates a new CSV file with headers for subject, body, and category
    if the file doesn't already exist.
    """
    if not os.path.exists(TRAINING_DATA_PATH):
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(TRAINING_DATA_PATH), exist_ok=True)
            
            with open(TRAINING_DATA_PATH, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["subject", "body", "category"])
            logger.info(f"Created new training data file at {TRAINING_DATA_PATH}")
        except Exception as e:
            logger.error(f"Error creating training data file: {e}")
            raise


def append_to_training_data(subject, body, category):
    """
    Append categorized email data to the training data file.

    Args:
        subject: The email subject.
        body: The email body.
        category: The assigned category.
    """
    try:
        # Initialize the file if it doesn't exist
        if not os.path.exists(TRAINING_DATA_PATH):
            initialize_training_data()
            
        with open(TRAINING_DATA_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([subject, body, category])
        logger.info(f"Added new training data entry with category: {category}")
    except Exception as e:
        logger.error(f"Error appending to training data: {e}")