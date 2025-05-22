import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

from .llm_service import LLMService
from .config import USER_INFO, LOG_LEVEL, LOG_FORMAT
from .connector import update_draft_status, check_draft_created

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def generate_response(prompt, max_tokens=1000):
    """
    Generate a response using the configured LLM provider.

    Args:
        prompt: The prompt to send to the LLM.
        max_tokens: Maximum number of tokens to generate.

    Returns:
        The generated text response.
    """
    try:
        # Initialize the LLM service with the configured provider
        llm_service = LLMService()

        # Generate the response
        return llm_service.generate_text(prompt, max_tokens)
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        # Return a fallback response
        return f"I apologize, but I'm unable to generate a response at this time due to a technical issue."

def truncate_text(text, max_tokens=2000):
    """
    Truncate the text to fit within the model's maximum token limit.
    """
    words = text.split()
    return " ".join(words[:max_tokens])

def auto_respond(service, subject, body, category, message_id, sender_email):
    """
    Prepare an auto-response using the configured LLM and save it in drafts.

    Args:
        service: The Gmail API service object.
        subject: The email subject.
        body: The email body.
        category: The category of the email.
        message_id: The Gmail message ID.
        sender_email: The email address of the sender.
    """
    logger.info(f"Processing email with category: {category}")

    # Check if we've already created a draft for this message
    if check_draft_created(message_id):
        logger.info(f"Draft already created for message {message_id}, skipping")
        return

    if category in ["urgent response", "very important", "important"]:
        # Combine subject and body
        prompt = f"""You are a professional assistant. Generate a polite and professional email response based on the following email:
        Subject: {subject}
        Body: {body}
        your Name: "{USER_INFO['name']}"
        your Position: "{USER_INFO['position']}"
        your Contact: "{USER_INFO['contact']}"
        your company: "{USER_INFO['company']}"

        take the Recipient's Name from the context
        """

        # Truncate the prompt if necessary
        truncated_prompt = truncate_text(prompt, max_tokens=2000)

        # Generate response using configured LLM
        auto_response_body = generate_response(truncated_prompt)

        logger.info(f"Generated response for email with subject: {subject}")

        try:
            # Create the draft and save in Gmail
            message = MIMEMultipart()
            message["to"] = sender_email
            message["subject"] = f"Re: {subject}"
            message.attach(MIMEText(auto_response_body, "plain"))

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            draft = {"message": {"raw": raw_message}}
            draft_response = service.users().drafts().create(userId="me", body=draft).execute()
            logger.info(f"Draft created with ID: {draft_response.get('id')}")
            
            # Update the database to mark that we've created a draft
            update_draft_status(message_id)
        except Exception as e:
            logger.error(f"Error creating draft: {e}")

    else:
        logger.info(f"Email category '{category}' does not require an auto-response.")
        try:
            # Mark email as read
            service.users().messages().modify(
                userId='me', 
                id=message_id, 
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.info(f"Email marked as read: {message_id}")
        except Exception as e:
            logger.error(f"Error marking email as read: {e}")