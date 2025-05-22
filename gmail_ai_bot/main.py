import logging
import argparse
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from .bot import authenticate_gmail, process_unread_emails
from .config import POLLING_INTERVAL_MINUTES, LOG_LEVEL, LOG_FORMAT
from . import app

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def job():
    """
    Main job function that authenticates with Gmail and processes unread emails.
    This function is called periodically by the scheduler.
    """
    try:
        logger.info("Starting email processing job")
        service = authenticate_gmail()
        process_unread_emails(service)
        logger.info("Email processing job completed successfully")
    except Exception as e:
        logger.error(f"Error in email processing job: {e}")

def run_process():
    """Run the email processing job once and then start the scheduler."""
    try:
        job()
        # Initialize scheduler
        scheduler = BlockingScheduler()

        # Add job to run at the configured interval
        scheduler.add_job(job, "interval", minutes=POLLING_INTERVAL_MINUTES)

        logger.info(f"Starting scheduler with {POLLING_INTERVAL_MINUTES} minute interval")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Error in scheduler: {e}")

def run_auth():
    """Run the authentication server."""
    app.run()

def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(description="Gmail AI Bot - Email automation with AI")
    parser.add_argument("--auth", action="store_true", help="Start the authentication server")
    parser.add_argument("--process", action="store_true", help="Start the email processing service")
    
    args = parser.parse_args()
    
    if args.auth:
        run_auth()
    elif args.process:
        run_process()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()