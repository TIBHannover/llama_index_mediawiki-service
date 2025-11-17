import time
from flask import request, jsonify, stream_with_context
import json
from webhookParser import WebhookParser

def _check_bearer_token(auth_header: str) -> bool:
    try:
        token = auth_header.split(None, 1)[1]
        expected_token = os.getenv("MW_BEARER_TOKEN")
        return token == expected_token
    except Exception:
        return False

def require_auth(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if auth_header.lower().startswith("bearer ") and _check_bearer_token(auth_header):
            return view_func(*args, **kwargs)

        return _unauthorized_response()

    return wrapper


def _unauthorized_response():
    resp = make_response(jsonify({"error": "Unauthorized"}), 401)
    return resp


class MediawikiLLMAPI:
    def __init__(self, app,  MediawikiLLM):
        @app.route('/query', methods=['GET'])
        @require_auth
        def run_query():
            query = request.args.get('query')
            print(query)
            response = MediawikiLLM.query_engine.query(query)
            print(response)
            return jsonify(response.response)

        @app.route('/llm', methods=['GET'])
        def run_query_on_llm():
            query = request.args.get('query')
            print(query)
            response = MediawikiLLM.service_context.llm.complete(query)
            print(response)
            return jsonify(response.text)

        @app.route('/webhook', methods=['POST'])
        def webhook():
            content = json.loads(request.data)['content']
            type, page_url = WebhookParser.parse(content=content)

            if (type == ""):
                return ('error in webhook', 400)
            else:
                MediawikiLLM.updateVectorStore(type, page_url)
                return ('', 204)

        app.run(host='0.0.0.0', port=5000, debug=False)
