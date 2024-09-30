import os
from flask import Flask
from flask_cors import CORS
from MediawikiLLM import MediawikiLLM  # Import the MediawikiLLM class
from api import MediawikiLLMAPI  # Import the API class to manage Flask routes
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Initialize the MediawikiLLM class with the MediaWiki URLs from the environment variables
MWLLM = MediawikiLLM(
    os.getenv("MEDIAWIKI_URL"),  # MediaWiki URL
    os.getenv("MEDIAWIKI_API_URL")  # MediaWiki API URL
)

# Initialize the LLM with MediaWiki data. This method loads or creates the index.
MWLLM.init_from_mediawiki()

# Create the Flask app instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask app
# This allows the API to accept requests from different domains
CORS(app)

# Initialize the API routes by passing the Flask app and the MediawikiLLM instance
api = MediawikiLLMAPI(app, MWLLM)

# If you run the app.py directly, it starts the Flask server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # Run the Flask app on all network interfaces and port 5000
