"""
llm model classes.
"""

import os
from langchain_openai import ChatOpenAI


class LlmOpenAI:
    def create_model():
        llm = ChatOpenAI(
                temperature=0, 
                model_name='gpt-3.5-turbo',
                openai_api_key=os.environ.get('OPENAI_API_KEY')
            )
        return llm