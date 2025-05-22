# Gmail AI Bot

An intelligent email assistant that automatically categorizes and responds to emails based on their importance.

## Features

- **Email Categorization**: Automatically categorizes incoming emails using a transformer-based model
- **Smart Responses**: Generates professional responses to important emails using LLM technology
- **Multiple LLM Options**: Supports various LLM providers (Ollama, OpenAI, Google Gemini, HuggingFace)
- **Flexible Configuration**: Easily configurable through environment variables
- **Training Data Collection**: Collects categorized emails for future model training
- **Database Storage**: Stores processed emails in a SQLite database

## Installation

```bash
pip install gmail-ai-bot
```

## Quick Start

1. Create a `.env` file with your configuration:

```
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5-coder
POLLING_INTERVAL_MINUTES=5
USER_NAME=Your Name
USER_POSITION=Your Position
USER_COMPANY=Your Company
```

2. Place your Gmail API `credentials.json` file in your working directory

3. Start the authentication server:

```python
from gmail_ai_bot import app
app.run()
```

4. Visit `http://localhost:8080` in your browser and authenticate with Gmail

5. Start the email processing service:

```python
from gmail_ai_bot import main
main.run()
```

## Command Line Usage

After installation, you can also use the command line interface:

```bash
# Start the authentication server
gmail-ai-bot --auth

# Start the email processing service
gmail-ai-bot --process
```

## LLM Provider Options

The application supports multiple LLM providers with different cost implications:

### Ollama (Free, Local)
- Runs locally on your machine
- No API costs
- Requires more system resources
- Default model: qwen2.5-coder
- Setup: Install Ollama from [ollama.ai](https://ollama.ai)

### OpenAI (Paid)
- High-quality responses
- Pay-per-token pricing
- Default model: gpt-3.5-turbo
- Setup: Get API key from [OpenAI](https://platform.openai.com)

### Google Gemini (Paid, with Free Tier)
- Competitive quality
- Free tier available (limited usage)
- Default model: gemini-pro
- Setup: Get API key from [Google AI Studio](https://makersuite.google.com)

### HuggingFace (Mix of Free and Paid)
- Various models available
- Some models have free inference API
- Default model: mistralai/Mistral-7B-Instruct-v0.2
- Setup: Get API key from [HuggingFace](https://huggingface.co)

## Configuration

All configuration is done through environment variables or a `.env` file.

Key configuration options:

- `LLM_PROVIDER`: Choose between 'ollama', 'openai', 'google', or 'huggingface'
- `POLLING_INTERVAL_MINUTES`: How often to check for new emails
- `EMAIL_CATEGORIES`: Categories for email classification
- `USER_NAME`, `USER_POSITION`, etc.: Your information for email signatures

## API Reference

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

# Categorize an email
from gmail_ai_bot import categorize_email
category = categorize_email(subject, body)

# Generate a response
from gmail_ai_bot import auto_respond
auto_respond(service, subject, body, category, message_id, sender_email)
```

## License

MIT