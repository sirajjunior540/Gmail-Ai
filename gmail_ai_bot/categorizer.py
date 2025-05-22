import logging
from transformers import pipeline
from .config import CATEGORIZATION_MODEL, EMAIL_CATEGORIES, MAX_TEXT_LENGTH, LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize the classifier with the configured model
# Use lazy loading to avoid initializing the model until it's needed
classifier = None

def get_classifier():
    """
    Get the text classification pipeline, initializing it if necessary.
    
    Returns:
        The text classification pipeline.
    """
    global classifier
    if classifier is None:
        try:
            classifier = pipeline("text-classification", model=CATEGORIZATION_MODEL, top_k=None)
            logger.info(f"Initialized categorization model: {CATEGORIZATION_MODEL}")
        except Exception as e:
            logger.error(f"Error initializing categorization model: {e}")
            raise
    return classifier

def truncate_text(text, max_length=MAX_TEXT_LENGTH):
    """
    Truncate text to the specified maximum length.

    Args:
        text: The text to truncate.
        max_length: Maximum length of the text.

    Returns:
        The truncated text.
    """
    return text[:max_length]

def categorize_email(subject, body, labels=None, max_length=MAX_TEXT_LENGTH):
    """
    Categorize an email based on its subject and body.

    Args:
        subject: The email subject.
        body: The email body.
        labels: Dictionary of category labels. If None, uses EMAIL_CATEGORIES from config.
        max_length: Maximum length of text to process.

    Returns:
        The predicted category of the email.
    """
    # Use configured categories if none provided
    if labels is None:
        labels = EMAIL_CATEGORIES

    try:
        # Combine subject and body
        text = f"Subject: {subject}\n\nBody: {body}"
        truncated_text = truncate_text(text, max_length)

        # Get predictions from the model
        model = get_classifier()
        predictions = model(truncated_text)

        # Map predictions to categories
        categories = list(labels.keys())
        category_scores = {categories[i]: predictions[0][i]['score'] for i in range(len(categories))}

        # Get the category with the highest score
        best_category = max(category_scores, key=category_scores.get)

        logger.info(f"Categorized email with subject '{subject[:30]}...' as '{best_category}'")
        return best_category

    except Exception as e:
        logger.error(f"Error categorizing email: {e}")
        # Return a default category in case of error
        return list(labels.keys())[0]