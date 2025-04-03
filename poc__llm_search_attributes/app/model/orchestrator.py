"""
llm orchestrator library.
"""
from typing import List

from app.db.database import get_db

from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from app.model.prompts import system_message, query_template
from app.model.models import LlmOpenAI




class LlmOrchestrator:
    def __init__(self):
        self.llm =  LlmOpenAI.create_model()  # set language model here
        self.db = get_db()
        self.db_chain = SQLDatabaseChain.from_llm(
            llm=self.llm, 
            db=self.db, 
            verbose=True
        )
    
    def _retrieve_from_db(self, query: str) -> str:
        """creates a db context"""
        context = self.db_chain(query)
        context = context['result'].strip()
        return context


    def _build_prompt(self, query: str, context: any) -> List:
        """builds a chat prompt"""
        human_query_template = HumanMessagePromptTemplate.from_template(
            template=query_template
        )
        messages = [
            SystemMessage(content=system_message),
            human_query_template.format(human_input=query, db_context=context)
        ]  
        return messages


    def generate_response(self, query: str) -> str:
        """executes query with context"""
        context = self._retrieve_from_db(query=query)
        messages = self._build_prompt(query=query, context=context)

        resp = self.llm(messages).content
        return resp


# if __name__== '__main__':
#     query = "Which candidates have a long hair style and red hair color and a height between 150 and 170 cm?"
    
#     llm_orchestrator = LlmOrchestrator()
#     resp = llm_orchestrator.generate_response(
#         query=query
#     )
