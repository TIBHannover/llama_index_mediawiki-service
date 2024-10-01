from reader.MediawikiPagesReader import MediawikiPagesReader


class DocumentClass():
    api_url = None
    reader = MediawikiPagesReader()
    documents = []

    def __init__(self, api_url):
        self.api_url = api_url

    def mediawiki_get_all_pages(self, url: str):
        self.documents = self.reader.init_document(self.api_url, url)

    def mediawiki_get_single_page(self, page_url: str):
        return self.reader.get_single_page(self.api_url, page_url)

    def mediawiki_update_page(self, page_url):
        updated_document_list = self.mediawiki_get_single_page(page_url)

        for i, doc in enumerate(self.documents):
            if doc.doc_id.startswith(page_url):
                self.documents.clear(doc)
                break
        
        self.documents = self.document + updated_document_list

    def mediawiki_delete_page(self, page_url):
        self.documents = [
            doc for doc in self.documents if not doc.doc_id.startswith(page_url)]
