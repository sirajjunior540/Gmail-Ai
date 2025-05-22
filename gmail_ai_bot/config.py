"""
Configuration file for the Gmail AI Bot
Contains settings for:
- LLM providers and models
- Email processing
- Database
- Authentication
- Logging
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Helper function to get file paths that work both in development and when installed as a package
def get_file_path(filename, default_dir=None):
    # First check if file exists in current working directory
    cwd_file = Path(os.getcwd()) / filename
    if cwd_file.exists():
        return str(cwd_file)
    
    # Then check if a default directory was provided
    if default_dir:
        default_file = Path(default_dir) / filename
        if default_file.exists():
            return str(default_file)
    
    # Return the filename as is (will be looked for in current directory)
    return filename

# LLM Configuration
# Options: 'ollama', 'openai', 'google', 'huggingface'
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')

# Model configuration for different providers
LLM_CONFIG = {
    'ollama': {
        'model': os.getenv('OLLAMA_MODEL', 'qwen2.5-coder'),
        'api_base': os.getenv('OLLAMA_API_BASE', 'http://localhost:11434'),
    },
    'openai': {
        'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'api_key': os.getenv('OPENAI_API_KEY', ''),
    },
    'google': {
        'model': os.getenv('GOOGLE_MODEL', 'gemini-pro'),
        'api_key': os.getenv('GOOGLE_API_KEY', ''),
    },
    'huggingface': {
        'model': os.getenv('HF_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2'),
        'api_key': os.getenv('HF_API_KEY', ''),
        'provider': os.getenv('HF_PROVIDER', 'auto'),
    }
}

# Email categorization model
CATEGORIZATION_MODEL = os.getenv('CATEGORIZATION_MODEL', 'bhadresh-savani/distilbert-base-uncased-emotion')

# Email categories and their descriptions
EMAIL_CATEGORIES = {
    'urgent response': 'Emails requiring immediate attention and response',
    'not important': 'Emails that can be safely ignored or processed later'
}

# Email processing settings
MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', 512))
POLLING_INTERVAL_MINUTES = int(os.getenv('POLLING_INTERVAL_MINUTES', 15))

# Database settings
DB_PATH = os.getenv('DB_PATH', 'sqlite:///database.db')
DB_ECHO = os.getenv('DB_ECHO', 'True').lower() in ('true', 'yes', '1')

# Gmail API settings
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_FILE = get_file_path(os.getenv('TOKEN_FILE', 'token.pickle'))
CREDENTIALS_FILE = get_file_path(os.getenv('CREDENTIALS_FILE', 'credentials.json'))

# Flask settings
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
FLASK_PORT = int(os.getenv('FLASK_PORT', 8080))

# Training data settings
TRAINING_DATA_PATH = get_file_path(os.getenv('TRAINING_DATA_PATH', 'email_training_data.csv'))

# User information for email responses
USER_INFO = {
    'name': os.getenv('USER_NAME', 'Abdallah Ahmed'),
    'position': os.getenv('USER_POSITION', 'CTO'),
    'contact': os.getenv('USER_CONTACT', '+971503950224'),
    'company': os.getenv('USER_COMPANY', 'Al Kushk')
}

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')