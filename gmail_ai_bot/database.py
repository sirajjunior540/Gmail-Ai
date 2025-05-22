import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DB_PATH, DB_ECHO, LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Define database engine
logger.info(f"Initializing database with path: {DB_PATH}, echo: {DB_ECHO}")
engine = create_engine(DB_PATH, echo=DB_ECHO)

# Define Base for ORM models
Base = declarative_base()

# Define the Emails model
class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(255), unique=True, nullable=False)
    thread_id = Column(String(255), nullable=False)
    subject = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)
    draft_created = Column(Boolean, default=False)

# Create the table
Base.metadata.create_all(engine)

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Export the session and Base for use in other modules
def get_session():
    """Get a new database session."""
    return Session()