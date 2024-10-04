import logging
import os

# Configure logging
log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=log_level)

# Create a logger instance
logger = logging.getLogger(__name__)
