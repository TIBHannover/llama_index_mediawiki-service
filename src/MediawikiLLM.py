import os
import time
from llama_index import ServiceContext, StorageContext, VectorStoreIndex, load_index_from_storage, set_global_service_context
from llama_index.vector_stores import FaissVectorStore
import llama_index
from Models import Models
from DocumentClass import DocumentClass
import faiss

class MediawikiLLM:

    service_context = None
    mediawiki_url = None
    api_url = None

    DocumentClass = None
    index = None
    index_filename = None
    query_engine = None

    def __init__(self, mediawiki_url, api_url):

        self.mediawiki_url = mediawiki_url
        self.DocumentClass = DocumentClass(api_url)

        llm = Models.CreateLlamaCCP(
            model_url=os.getenv("MODEL_URL"), model_path=os.getenv("MODEL_PATH"))

        # llm = Models.CreateHuggingFaceLLM(model_name="Writer/camel-5b-hf")

        self.service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model="local",
            chunk_size=1024,
        )

    def init_from_mediawiki(self):
        set_global_service_context(self.service_context)

        d = 1536
        faiss_index = faiss.IndexFlatL2(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)

        if os.path.isdir(str(os.getenv("PERSISTENT_STORAGE_DIR"))):
            storage_context = StorageContext.from_defaults(
                persist_dir=os.getenv("PERSISTENT_STORAGE_DIR"), vector_store=vector_store)
            self.index = load_index_from_storage(storage_context)
        else:
            self.DocumentClass.mediawiki_get_all_pages(self.mediawiki_url)

            self.index = VectorStoreIndex.from_documents(
                self.DocumentClass.documents, service_context=self.service_context)
            if os.getenv("PERSISTENT_STORAGE_DIR") is not None:
                self.index.storage_context.persist(
                    os.getenv("PERSISTENT_STORAGE_DIR"))

        self.query_engine = self.index.as_query_engine()

    def init_no_documents(self):
        self.index = llama_index.indices.empty.EmptyIndex(
            service_context=self.service_context)
        self.query_engine = self.index.as_query_engine()

    def updateVectorStore(self, type: str, page_url: str):
        if type == 'edit' or type == 'create':
            print("create/edit " + page_url)
            self.DocumentClass.mediawiki_update_page(page_url)

        elif type == 'delete':
            print("delete " + page_url)
            self.DocumentClass.mediawiki_delete_page(page_url)

        self.index.refresh(self.DocumentClass.documents)
