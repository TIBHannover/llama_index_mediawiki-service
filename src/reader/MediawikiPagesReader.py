"""Simple reader that reads MediaWiki."""
import os
from typing import Any, Dict, List
import html2text

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
import requests


class MediawikiPagesReader(BaseReader):
    """MediawikiAllPagesReader reader.

    Reads all pages.

    """

    def init_document(
        self, apiUrl: str, url: str, **load_kwargs: Any
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            apiUrl (str): URL of api.php.
            url  (str): base of wiki
        """
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
                    data = response.json()
                    pages = data["query"]["allpages"]
                    for page in pages:
                        title = page["title"]
                        print(title)
                        response = requests.get(url + title, headers=None)
                        documents.append(
                            Document(text=response.text, doc_id=url+title))

                    if "continue" not in data:
                        break

                    params["apcontinue"] = data["continue"]["apcontinue"]

        return documents

    def get_single_page(self, apiUrl: str, pageUrl: str, **load_kwargs: Any):
        response = requests.get(pageUrl, headers=None).text
        response = html2text.html2text(response)
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
