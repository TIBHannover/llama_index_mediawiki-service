import os
import time
from flask import request, jsonify, stream_with_context, Response
from flask_httpauth import HTTPBasicAuth
import json

import requests
from webhookParser import WebhookParser

# Initialize the Flask HTTPBasicAuth object
auth = HTTPBasicAuth()

# Define the verification function for Basic Auth
@auth.verify_password
def verify_password(username, password):
    # Extract "wiki_session" from the request's cookies
    wiki_session = request.cookies.get('wiki_session')

    if not wiki_session:
        return None  # No session token provided

    # Define the MediaWiki API endpoint for validating the session
    apiUrl = os.getenv("MEDIAWIKI_API_URL")  # Replace with your actual MediaWiki API URL
    
    # Create session object to retain cookies
    session = requests.Session()
    
    # Pass the session token as a cookie to MediaWiki's API
    for cookie_name, cookie_value in request.cookies.items():
        if cookie_name.startswith('wiki'):
            session.cookies.set(cookie_name, cookie_value)
    
    # Prepare API call to verify session
    params = {
        'action': 'query',
        'meta': 'userinfo',
        'format': 'json'
    }

    # Send the request to MediaWiki API with the session cookie
    response = session.get(apiUrl, params=params)
    
    # Check if the response is 200 OK, which means the session is valid
    if response.status_code == 200:
        user_info = response.json().get('query', {}).get('userinfo', {})
        if 'id' in user_info and user_info['id'] > 0:
            # User is valid, return the username for authentication
            return user_info.get('name', None)
    
    # Invalid session or bad response
    return None

class MediawikiLLMAPI:
    def __init__(self, app, MediawikiLLM):
        @app.route('/query', methods=['GET'])
        @auth.login_required  
        def run_query():
            query = request.args.get('query')
            print(query)
            response = MediawikiLLM.query_engine.query(query)
            print(response)
            return jsonify(response.response)

        @app.route('/llm', methods=['GET'])
        # @auth.login_required 
        def run_query_on_llm():
            query = request.args.get('query')
            print(query)
            response = MediawikiLLM.service_context.llm.complete(query)
            print(response)
            return jsonify(response.text)

        @app.route('/webhook', methods=['POST'])
        # @auth.login_required  
        def webhook():
            content = json.loads(request.data)['content']
            type, page_url = WebhookParser.parse(content=content)

            if type == "":
                return ('error in webhook', 400)
            else:
                MediawikiLLM.updateVectorStore(type, page_url)
                return ('', 204)

        app.run(host='0.0.0.0', port=5000, debug=False)

