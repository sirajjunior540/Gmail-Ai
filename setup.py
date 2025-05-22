from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gmail-ai-bot",
    version="0.1.0",
    author="Gmail AI Bot Team",
    author_email="example@example.com",
    description="An intelligent email assistant that automatically categorizes and responds to emails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gmail-ai-bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=3.1.0",
        "APScheduler>=3.11.0",
        "SQLAlchemy>=2.0.32",
        "python-dotenv>=1.0.1",
        "google-api-python-client>=2.143.0",
        "google-auth>=2.34.0",
        "google-auth-httplib2>=0.2.0",
        "google-auth-oauthlib>=1.2.1",
        "ollama>=0.4.5",
        "openai>=1.43.0",
        "google-generativeai>=0.7.2",
        "huggingface-hub>=0.27.0",
        "transformers>=4.47.1",
        "torch>=2.5.1",
        "tqdm>=4.66.5",
        "pydantic>=2.8.2",
        "PyYAML>=6.0.2",
    ],
    entry_points={
        "console_scripts": [
            "gmail-ai-bot=gmail_ai_bot.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gmail_ai_bot": ["*.json", "*.csv"],
    },
)