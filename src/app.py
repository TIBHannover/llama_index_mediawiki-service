import os
from flask import Flask
from flask_cors import CORS
from MediawikiLLM import MediawikiLLM  # Import the MediawikiLLM class
from api import MediawikiLLMAPI  # Import the API class to manage Flask routes
from dotenv import load_dotenv  # To load environment variables from a .env file
from logger import logger

# Load environment variables from a .env file
load_dotenv()

logger.debug("Starting MediawikiLLM initialization...")

# Initialize the MediawikiLLM class with the MediaWiki URLs from the environment variables
MWLLM = MediawikiLLM(
    os.getenv("MEDIAWIKI_URL"),  # MediaWiki URL
    os.getenv("MEDIAWIKI_API_URL")  # MediaWiki API URL
)

logger.debug("MediawikiLLM instance created.")
MWLLM.init_from_mediawiki()
logger.debug("MediawikiLLM initialized from MediaWiki.")

# Create the Flask app instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask app
CORS(app)

# Initialize the API routes by passing the Flask app and the MediawikiLLM instance
api = MediawikiLLMAPI(app, MWLLM)

logger.debug("Flask app initialized and routes set.")

# If you run the app.py directly, it starts the Flask server
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)  # Enable debug for detailed logging
