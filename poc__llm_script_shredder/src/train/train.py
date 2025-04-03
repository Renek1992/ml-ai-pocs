"""
Script for extraction of training data.
"""
import re
import os
import json
import ollama
from datetime import datetime
from openai import OpenAI
from PyPDF2 import PdfReader
from src.shared.telemetry.logs.logging import PythonLogger


logger = PythonLogger.get_logger(log_level="INFO", name="script-shredder-train")



def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    
    pdf_text = ""
    
    reader = PdfReader(stream=pdf_path)
    number_of_pages = len(reader.pages)
    for page_num in range(number_of_pages):
        page = reader.pages[page_num]
        pdf_text += page.extract_text()

    logger.info(f"Loaded pdf from {pdf_path} with total word count of {len(pdf_text.split())}")
    return pdf_text



def get_openai_response(context: str):
    template = """
    You are supposed to extract all information of characters in a given script that is provided as 
    context here. Process the following context and return only an array of json objects. The individual 
    json object should have a key of: 
        - 'role_name' (Name of the character)
        - 'role_description' (Brief description of the character)
        - 'scene_count' (Count the number of scenes the character appears in)
        - 'gender' (Gender of the character)
        - 'minimum_playable_age' (minimum potential age of the character)
        - 'maximum_playable_age' (maximum potential age of the character)
        - 'skills' (Any particular skills required)
        - 'demographics' (Demographic background of the character)
        - 'ethnicity' (Ethnic background of the character, which is either Aisan, Caucasian, Black, Hispanic, or Other)
    If any information about these keys dcan't be found then use 'N/A' but always include all keys.
    

    Script context: {context}
    """
    prompt = template.format(context=context)

    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    resp = completion.choices[0].message.content
    match = re.search(r'\[.*\]', resp, re.DOTALL)
    print(resp)
    if match:
        json_string = match.group(0)
        json_array = json.loads(json_string)
    else:
        json_array = json.loads(resp)

    return json_array




if __name__ == '__main__':
    pdf_path = './data/Progressive-Breakdown.pdf'
    context = str(extract_text_from_pdf(pdf_path=pdf_path)).replace('"', '')
    script_resp = get_openai_response(context=context)

    result = {
        'script_path' : pdf_path,
        'script_details' : script_resp,
        'script_context' : str(context),
        'processing_timestamp' : str(datetime.now()) 
    }

    second_slash_pos = pdf_path.find('/', pdf_path.find('/') + 1)
    pdf_pos = pdf_path.find('.pdf')
    substring = pdf_path[second_slash_pos + 1:pdf_pos]

    with open(f'./results/{substring}.json', 'w') as file:
        json.dump(result, file, indent=4)
    file.close()

    logger.info(f'./results/{substring}.json stored.')