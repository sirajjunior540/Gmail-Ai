import base64
import logging
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .categorizer import categorize_email
from .responser import auto_respond
from .connector import save_message_to_db
from .utils import initialize_training_data, append_to_training_data
from .config import GMAIL_SCOPES, TOKEN_FILE, CREDENTIALS_FILE, EMAIL_CATEGORIES, LOG_LEVEL, LOG_FORMAT

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def authenticate_gmail(redirect=False, code=None):
    """
    Authenticate with Gmail API and return the service object.

    Args:
        redirect (bool): If True, return the authorization URL instead of running a local server
        code (str): Authorization code from OAuth callback

    Returns:
        The authenticated Gmail API service object or authorization URL if redirect=True.
    """
    creds = None

    # Try to load credentials from token file
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            logger.info(f"Loaded credentials from {TOKEN_FILE}")
        except Exception as e:
            logger.error(f"Error loading credentials from {TOKEN_FILE}: {e}")

    # Refresh or create new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Refreshed expired credentials")
            except Exception as e:
                logger.error(f"Error refreshing credentials: {e}")
                creds = None

        # If still no valid credentials, run the OAuth flow
        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, GMAIL_SCOPES)
                
                if redirect:
                    # For web applications, return the authorization URL
                    auth_url, _ = flow.authorization_url(
                        access_type='offline',
                        include_granted_scopes='true'
                    )
                    return auth_url
                
                elif code:
                    # Use the authorization code from the callback
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    logger.info("Created new credentials from authorization code")
                
                else:
                    # For local applications, run the local server flow
                    creds = flow.run_local_server(port=8080)
                    logger.info("Created new credentials via OAuth flow")
                    
            except Exception as e:
                logger.error(f"Error in OAuth flow: {e}")
                raise

        # Save the credentials for future use
        if creds and not redirect:
            try:
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                logger.info(f"Saved credentials to {TOKEN_FILE}")
            except Exception as e:
                logger.error(f"Error saving credentials to {TOKEN_FILE}: {e}")

    # If we're just getting the auth URL, we don't need to build the service
    if redirect:
        return None

    # Build and return the Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail API service created successfully")
        return service
    except Exception as e:
        logger.error(f"Error building Gmail API service: {e}")
        raise


def get_message_subject_body_and_sender(message):
    """Extract the subject, body, and sender email of the email."""
    subject, body, sender = '', '', ''
    for header in message.get('payload', {}).get('headers', []):
        if header['name'].lower() == 'subject':
            subject = header['value']
        elif header['name'].lower() == 'from':
            sender = header['value']

    body_data = message.get('payload', {}).get('body', {}).get('data', '')
    if body_data:
        body = base64.urlsafe_b64decode(body_data).decode('utf-8')

    return subject, body, sender


def process_unread_emails(service):
    """
    Process unread emails from the inbox.

    Args:
        service: The authenticated Gmail API service object.
    """
    # Initialize training data file if it doesn't exist
    initialize_training_data()

    try:
        # Get unread messages from inbox
        results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
        messages = results.get('messages', [])

        if not messages:
            logger.info("No unread messages found.")
            return

        logger.info(f"Found {len(messages)} unread messages to process")

        # Process each unread message
        for msg in messages:
            try:
                # Get message details
                message = service.users().messages().get(userId='me', id=msg['id']).execute()
                message_id, thread_id = msg['id'], message['threadId']
                subject, body, sender = get_message_subject_body_and_sender(message)

                logger.info(f"Processing email: {subject[:30]}... from {sender}")

                # Categorize the email
                category = categorize_email(subject, body)

                # Save to database and training data
                save_message_to_db(message_id, thread_id, subject, body, category)
                append_to_training_data(subject, body, category)

                # Generate and save response if needed
                auto_respond(service, subject, body, category, message_id, sender)

                logger.info(f"Successfully processed email with ID: {message_id}")

            except Exception as e:
                logger.error(f"Error processing message {msg['id']}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error listing unread messages: {e}")