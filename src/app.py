import os
from flask import Flask
from flask_cors import CORS
from MediawikiLLM import MediawikiLLM
from api import MediawikiLLMAPI

from dotenv import load_dotenv

load_dotenv()

MWLLM = MediawikiLLM(os.getenv("MEDIAWIKI_URL"),
                     os.getenv("MEDIAWIKI_API_URL"))
MWLLM.init_from_mediawiki()


app = Flask(__name__)
CORS(app)
api = MediawikiLLMAPI(app, MWLLM)
