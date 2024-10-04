"""Simple reader that reads MediaWiki."""
from logger import logger

import os
from typing import Any, Dict, List
import html2text

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import requests
from bs4 import BeautifulSoup


class MediawikiPagesReader(BaseReader):
    """MediawikiAllPagesReader reader.

    Reads all pages.

    """

    def init_document(self, apiUrl: str, url: str, **load_kwargs: Any) -> List[Document]:
        """Load data from the input directory."""
        documents = []
        
        ns_whitelist = os.getenv("MEDIAWIKI_NAMESPACES").split(",")
        session = requests.Session()
        namespaces = self.get_namespaces(apiUrl)

        for ns_id, ns_name in namespaces.items():
            if str(ns_id) in ns_whitelist:
                params = {
                    "action": "query",
                    "format": "json",
                    "list": "allpages",
                    "aplimit": "max",
                    "apnamespace": ns_id,
                }

                apfrom = os.getenv("MEDIAWIKI_APFROM")
                apto = os.getenv("MEDIAWIKI_APTO")

                if apfrom:
                    params.update({"apfrom": apfrom})
                if apto:
                    params.update({"apto": apto})

                while True:
                    response = session.get(url=apiUrl, params=params)
                    logger.debug(f"Response for namespace {ns_id}: {response.json()}")
                    data = response.json()
                    
                    # Check if "query" and "allpages" exist in the response
                    if "query" in data and "allpages" in data["query"]:
                        pages = data["query"]["allpages"]
                        for page in pages:
                            title = page["title"]
                            logger.debug(f"getting {title}")

                            # Construct the URL with the correct format
                            page_url = f"{url}/{title}"  # Correctly format the URL with a "/" before the title
                            page_response = requests.get(page_url, headers=None)
                            
                            chunklist = self.create_document_from_chunks(page_response, page_url)
                            documents.extend(chunklist)
                    else:
                        logger.debug(f"No pages found for namespace {ns_id}. Response: {data}")

                    if "continue" not in data:
                        break

                    params["apcontinue"] = data["continue"]["apcontinue"]

        return documents



    def get_single_page(self, apiUrl: str, pageUrl: str, **load_kwargs: Any):
        response = requests.get(pageUrl, headers=None).text
        chunklist = self.create_document_from_chunks(response, pageUrl)
        return chunklist
        return Document(text=response, doc_id=pageUrl)

    def get_namespaces(self, apiUrl: str) -> Dict[int, str]:
        """
        Fetches the available namespaces from the MediaWiki API.

        Args:
            apiUrl (str): URL of the MediaWiki API endpoint.

        Returns:
            Dict[int, str]: A dictionary mapping namespace IDs to their names.
        """
        session = requests.Session()
        params = {
            "action": "query",
            "format": "json",
            "meta": "siteinfo",
            "siprop": "namespaces"
        }

        response = session.get(url=apiUrl, params=params)
        data = response.json()

        namespaces = data["query"]["namespaces"]
        return {int(ns_id): ns_info["*"] for ns_id, ns_info in namespaces.items()}

    def create_document_from_chunks(self, response, doc_id) -> List[Document]:
        soup = BeautifulSoup(response.text, "html.parser")
        documents = []
        logger.debug(f"Parsing document from {doc_id}. Response content: {response.text[:200]}...")  # Log the start of the response
        for count, chunk in enumerate(soup.find_all("div", class_='chunks'), start=1):
            # remove sup elements
            for sup in chunk.find_all("sup"):
                sup.decompose()
            documents.append(Document(text=chunk.get_text(), doc_id=doc_id + f"chunk{count}"))

        logger.debug(f"Found {len(documents)} chunks for {doc_id}.")  # Log the number of chunks found
        return documents

