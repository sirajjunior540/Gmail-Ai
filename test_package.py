#!/usr/bin/env python3
"""
Test script to verify that the gmail-ai-bot package can be installed and used.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all package components can be imported."""
    try:
        from gmail_ai_bot import (
            authenticate_gmail, 
            process_unread_emails, 
            LLMService, 
            categorize_email, 
            auto_respond
        )
        logger.info("Successfully imported main components from gmail_ai_bot")
        
        # Test importing submodules
        from gmail_ai_bot.config import LLM_PROVIDER
        from gmail_ai_bot.database import Email
        from gmail_ai_bot.connector import save_message_to_db
        from gmail_ai_bot.utils import initialize_training_data
        from gmail_ai_bot.categorizer import truncate_text
        from gmail_ai_bot.responser import generate_response
        from gmail_ai_bot.bot import get_message_subject_body_and_sender
        from gmail_ai_bot.llm_service import LLMService
        from gmail_ai_bot.main import job
        from gmail_ai_bot.app import app
        
        logger.info("Successfully imported all submodules")
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def test_llm_service():
    """Test creating an LLM service instance."""
    try:
        from gmail_ai_bot import LLMService
        
        # Create an instance with a mock provider to avoid actual API calls
        llm = LLMService(provider='huggingface', model='mock-model')
        logger.info(f"Successfully created LLMService instance with provider: {llm.provider}, model: {llm.model}")
        return True
    except Exception as e:
        logger.error(f"Error creating LLMService: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing gmail-ai-bot package...")
    
    import_success = test_imports()
    llm_success = test_llm_service()
    
    if import_success and llm_success:
        logger.info("All tests passed! The package structure appears to be correct.")
        sys.exit(0)
    else:
        logger.error("Some tests failed. Please check the package structure and dependencies.")
        sys.exit(1)