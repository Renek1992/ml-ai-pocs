from typing import Dict, List, Union

from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms import Bedrock
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class ChatClient:
    def __init__(self):
        self.model_id = "amazon.titan-text-express-v1"
        self.model_kwargs = {
            "temperature": 0.1
        }
        self.llm = Bedrock(
            model_id=self.model_id, 
            model_kwargs=self.model_kwargs, 
            streaming=True,
            region_name='us-east-1',
            callbacks=[StreamingStdOutCallbackHandler()]
        )