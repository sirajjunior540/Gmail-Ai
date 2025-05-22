"""
Gmail AI Bot - An intelligent email assistant

This package provides functionality to automatically categorize and respond to emails
based on their importance using various LLM providers.
"""

__version__ = '0.1.0'

# Import main components to make them available at the package level
from .bot import authenticate_gmail, process_unread_emails
from .llm_service import LLMService
from .categorizer import categorize_email
from .responser import auto_respond