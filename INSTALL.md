# Installing Gmail AI Bot

This document provides instructions for installing and using the Gmail AI Bot package.

## Installation

### From PyPI (recommended)

Once the package is published to PyPI, you can install it using pip:

```bash
pip install gmail-ai-bot
```

### From Source

To install the package from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gmail-ai-bot.git
   cd gmail-ai-bot
   ```

2. Install the package in development mode:
   ```bash
   cd gmail_ai_bot  # Enter the package directory
   pip install -e .
   ```

## Configuration

1. Create a `.env` file with your configuration:

```
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5-coder
POLLING_INTERVAL_MINUTES=5
USER_NAME=Your Name
USER_POSITION=Your Position
USER_COMPANY=Your Company
```

2. Place your Gmail API `credentials.json` file in your working directory. You can obtain this file from the [Google Cloud Console](https://console.cloud.google.com/) by creating a project and enabling the Gmail API.

## Usage

### Command Line Interface

After installation, you can use the command line interface:

```bash
# Start the authentication server
gmail-ai-bot --auth

# Start the email processing service
gmail-ai-bot --process
```

### Python API

You can also use the package as a Python library:

```python
# Authenticate with Gmail
from gmail_ai_bot import authenticate_gmail
service = authenticate_gmail()

# Process unread emails
from gmail_ai_bot import process_unread_emails
process_unread_emails(service)

# Use LLM service directly
from gmail_ai_bot import LLMService
llm = LLMService(provider='ollama', model='qwen2.5-coder')
response = llm.generate_text("Write a professional email response")
```

## Testing the Installation

To verify that the package is installed correctly, you can run the test script:

```bash
cd gmail_ai_bot  # Enter the package directory
python test_package.py
```

If all tests pass, the package is installed correctly.

## Troubleshooting

- **Authentication Issues**: Delete `token.pickle` and re-authenticate
- **LLM Connection Errors**: Check API keys and network connectivity
- **Missing Dependencies**: Ensure all requirements are installed
- **Import Errors**: Make sure the package is installed correctly