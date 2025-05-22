import logging
from .database import session, Email, get_session
from .config import LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def save_message_to_db(message_id, thread_id, subject, body, category, draft_created=False):
    """Save the message to the database if it hasn't been categorized yet."""
    try:
        if not session.query(Email).filter_by(message_id=message_id).first():
            new_email = Email(
                message_id=message_id,
                thread_id=thread_id,
                subject=subject,
                body=body,
                category=category,
                draft_created=draft_created
            )
            session.add(new_email)
            session.commit()
            logger.info(f"Saved message {message_id} to database")
        else:
            logger.info(f"Message {message_id} already exists in database")
    except Exception as e:
        logger.error(f"Error saving message to database: {e}")
        session.rollback()

def check_draft_created(message_id):
    """Check if a draft has already been created for this message."""
    try:
        return session.query(Email).filter_by(message_id=message_id, draft_created=True).first() is not None
    except Exception as e:
        logger.error(f"Error checking draft status: {e}")
        return False

def update_draft_status(message_id):
    """Update the database to indicate that a draft has been created for this message."""
    try:
        email = session.query(Email).filter_by(message_id=message_id).first()
        if email:
            email.draft_created = True
            session.commit()
            logger.info(f"Updated draft status for message {message_id}")
        else:
            logger.warning(f"Attempted to update draft status for non-existent message {message_id}")
    except Exception as e:
        logger.error(f"Error updating draft status: {e}")
        session.rollback()