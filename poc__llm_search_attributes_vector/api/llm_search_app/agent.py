"""

"""
import os
from typing import Dict
from api.llm_search_app.db.manager import DBManager
from langchain_community.vectorstores.lancedb import LanceDB

from api.common.logging import PythonLogger
from api.llm_search_app.models.embedding import EmbeddingClient, ModelFactory


class VectorEmbeddingBot:
    def __init__(
            self, 
            model_name: str, 
            model_kwargs: str ,
            query: str = None,
            no_profiles_to_embed: int = 10,
            no_of_matches: int = 4
    ) -> None:
        self.query = query
        self.logger = PythonLogger.get_logger(name='VectorSearch')
        
        self.embedding_model = ModelFactory.get_model(
            model_name=model_name, 
            model_kwargs=model_kwargs
        )
        self.db_manager = DBManager(self.logger)
        self.embeddings_client = EmbeddingClient(
            logger=self.logger, 
            model=self.embedding_model,
            no_profiles=no_profiles_to_embed
        )
        self.no_of_matches = no_of_matches

    
    def get_vector_search_results(self):
        self.logger.info(f"query: {self.query}")
        tbl = self.db_manager.open_table(os.environ.get('TBL_NAME'))
        vectorstore = LanceDB(connection=tbl, embedding=self.embedding_model)
        result = vectorstore.similarity_search(
            query=self.query,
            k=self.no_of_matches
            )
        return result


    def create_response(self):
        results = self.get_vector_search_results()
        if len(results) > 0:
            context = "\n\n---\n\n".join([doc.page_content for doc in results])
        else:
            context = "\n\n---\n\n"
        self.logger.info(f"\n\n{context}")
        return context
    

    def create_embeddings(self) -> Dict:
        try:
            resp = self.embeddings_client.store_vector_dataset()
            return resp
        except Exception as e:
            raise e