# User Manual

## Query
This section describes, how to query the service. After starting, the server displays the addresses of the API endpoint:
```
llama_index_mediawiki-flask-1  |  * Running on http://127.0.0.1:5000
llama_index_mediawiki-flask-1  |  * Running on http://172.23.0.2:5000
```
Example query: "When did SMWCon 2019 take place and where?"

### cURL

With Vector Index
```
> curl http://127.0.0.1:5000/query?query=When%20did%20SMWCon%202019%20take%20place%20and%20where%3F%20
```

Without Vector Index (query the LLM as is)
```
> curl http://127.0.0.1:5000/llm?query=When%20did%20SMWCon%202019%20take%20place%20and%20where%3F%20
```

### From Wiki
- see user manual of llama_index_mediawiki-ui MediaWiki extension
