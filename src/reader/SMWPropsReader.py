"""Simple reader that reads MediaWiki."""
import os
from typing import Any, Dict, List
import html2text


from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

import requests


class SMWPropsReader(BaseReader):
    """SMWPropsReader reader.

    Reads all SMW Properties.

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

                        data = {
                            'action': 'smwbrowse',
                            'format': 'json',
                            'browse': 'subject',
                            'params': '{"subject":"' + title + '","ns":0,"iw":"","subobject":"","options":{"dir":null,"lang":"de-formal","group":null,"printable":null,"offset":null,"including":false,"showInverse":false,"showAll":true,"showGroup":true,"showSort":false,"api":true,"valuelistlimit.out":"30","valuelistlimit.in":"20"},"type":"json"}'
                        }
                        response = requests.post(apiUrl, data=data, headers=None)
                        
                        properties_dict = {}

                        for prop in response.json()['query']['data']:
                            print(prop)
                            value = []
                            for innerVal in prop['dataitem']:
                                value.append(innerVal['item'])
                                
                            properties_dict[prop['property']] = value
                            
                        

                        for prop, value in properties_dict.items():

                            print(f"{prop}: {value}")
                            # Create a meaningful representation for the embedding
                            property_representation = f"has the property {prop} with the values: {', '.join(value)}"

                            documents.append(
                                Document(text=property_representation, doc_id=url + title)
                            )

                        # documents.append(
                        #     Document(text=response.text, doc_id=url+title))

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
