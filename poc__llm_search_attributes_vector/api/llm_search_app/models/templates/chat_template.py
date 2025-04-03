# Prompt Mgmt
from langchain.prompts import PromptTemplate

template = """
You are representing a Casting Agency recommending profiles based on certain criteria. 
Answer the question based only on the following context:

{context}


Human: {input}

Assistant:
"""

PROMPT = PromptTemplate(input_variables=["context", "input"], template=template)