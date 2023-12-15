# llama_index_mediawiki-service
llama_index_mediawiki-service is a container-virtualised service that aims to run a local Large Language Model (LLM) to assist wiki users.
The LLM is intended to act as a chatbot for a user and be aware of the content hosted on the wiki without sending that content to a third party service provider for privacy reasons.

It is intended to answer user questions such as "Where did the last 10 Semantic MediaWiki conferences take place?" or "Provide a top 5 list of event series with most events."

## Building Blocks
- [MediaWiki](https://mediawiki.org) - An open source wiki
- Wiki Database - A data store for the wiki, for example MySQL
- [LlamaIndex](https://www.llamaindex.ai/) - A data framework for connecting custom data sources to large language models (LLMs).
- A public available LLM
- A Vector Index created by LlamaIndex

See also [Architecture](docs/architecture.md)

## Project outcomes
The chosen solution approach has proven to be practicable. In particular, the initial filling of a vector index with the wiki's data and the subsequent event-driven updating form the basis for linking even large amounts of data to an existing LLM without the need for time-consuming training.

The selection of suitable models has a major influence on both speed and quality. In the tests, 13B/4-bit models proved to be well suited. However, it is important to ensure that sufficient RAM or video memory is available in both the "CPU" and "GPU" cases.

The connection of wiki data to the model (which was precisely the subject of this project) leads to a significant increase in response times. These are within a range that users are likely to find far too slow (more than 3 seconds). Further engineering on the Vector Index could possibly improve this.

In semantic wikis in particular, the wiki pages tend to contain little natural language text. For example, on the "Event" pages of confident-conference.org, the metadata of conferences is presented in tabular form in the form of name-value pairs. This presentation is not ideal for natural language queries. Here, the metadata could either be transferred directly to the Vector Index or inserted into the wiki pages as additional information via wiki templates. 


# Basic Architecture

The choices here are limited to langchain and llama_index.

For the specific task of teaching the LLM about our wiki context/content, we chose to use llama_index: https://www.llamaindex.ai/

"LlamaIndex solves this problem by connecting to these data sources and adding your data to the data that LLMs already have. This is often referred to as Retrieval-Augmented Generation (RAG). RAG allows you to use LLMs to query, transform and generate new insights from your data.

Using a custom-built reader that collects HTML pages from specific namespaces of a Mediawiki instance, we feed the LLMm with information from the wiki. 

Using a Flask endpoint, we can query the model and get a clear text response.

# Updating the data
As the Mediawiki data changes, the llama_index based application has a /webhook route to listen on.

This route parses webhook calls sent by the MediaWiki extension "Discord": https://www.mediawiki.org/wiki/Extension:Discord

For each insert, update or delete operation, the llama_index based application is notified by MediaWiki. Based on the action, it will delete, update or add the newly created page to the documents, and update the index, so that the LLM is always aware of new changes. (This has not been tested with very active MediaWiki servers...)


# Query
The application has a /query endpoint to which we can send a GET request with the parameter "query".
The endpoint will return the plain text response of the LLM response.

A special page has been created called LlamaPage, which can be found here: https://github.com/gesinn-it-evl/LlamaPage

After enabling this extension, we have the page http://wiki.local/index.php/Spezial:LlamaPage, which allows a user to query the endpoint and get a response. The endpoint is hardcoded to localhost:5000 for now. 

