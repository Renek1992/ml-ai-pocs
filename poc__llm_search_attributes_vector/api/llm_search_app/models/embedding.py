import os
import ast
import json
from time import sleep
import logging
from typing import List, Dict, Union
import boto3
import polars as pl
from tqdm import tqdm
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings

from api.llm_search_app.db.manager import DBManager
from api.llm_search_app.models.templates.embedding_template import EMBEDDING_TEMPLATE




class EmbeddingClient:
    def __init__(
            self, 
            logger: logging.Logger, 
            model: Union[BedrockEmbeddings, OpenAIEmbeddings], 
            no_profiles: int
    ) -> None:
        self.logger = logger
        self.embeddings = model
        self.db_manager = DBManager(logger=self.logger) 
        self.no_profiles = no_profiles


    def store_vector_dataset(self) -> None:
        results = self._create_vectors()
        try:
            self.db_manager.create_table(
                name=os.environ.get('TBL_NAME'),
                data=results)
        except Exception as e:
            raise e
        return {
            "result": f"Successfully stored {self.no_profiles} embeddings.",
            "data_preview" : results[:5]
        }


    def _create_vectors(self) -> List:
        df = self.db_manager.load_dataset().sort('RANK').limit(self.no_profiles)
        dict_list = df.to_dicts()
        results = []
        for item in tqdm(range(len(dict_list))):  
            text = str(self._create_text_string(dict_list[item]))
            result_dict = {
                'profile_id': dict_list[item]['PROFILE_ID'],
                'vector': self._create_embedding(
                    input=text,
                    type="query"
                ),
                'text': text
            }
            results.append(result_dict)
            self.logger.info(f"Embedding for profile_id: {dict_list[item]['PROFILE_ID']} created.")
        self.logger.info(pl.DataFrame(results).limit(10))
        return results


    def _create_text_string(self, items: Dict) -> str:
        gender_appearance = ' '.join(set(items['GENDER_APPEARANCE_LIST'].split())).replace("_", " ")
        ethnic_appearance = ' '.join(set(items['ETHNIC_APPEARANCE_LIST'].split())).replace("_", " ")

        resp_text = EMBEDDING_TEMPLATE.format(
            profile_id=items['PROFILE_ID'],
            profile_created=items['CREATED'],
            hair_style=items['HAIR_STYLE'].lower(),
            hair_color=items['HAIR_COLOR'].replace("_", " ").lower(),
            eye_color=items['EYE_COLOR'].lower(),
            height_cm=items['HEIGHT_CM'],
            weight_kg=items['WEIGHT_KG'],
            years_min=int(items['PLAYABLE_AGE_MIN_YEARS']),
            years_max=int(items['PLAYABLE_AGE_MAX_YEARS']),
            gender_appearance=gender_appearance.lower(),
            ethnic_appearance=ethnic_appearance.lower(),
            skills=self._build_skill_string(items['SKILL_LIST']),
            willingness=items['WILLINGNESS_LIST'].replace("_", " ").lower(),
            credits=self._build_credits_string(items['CREDITS'])
        )
        self.logger.debug(resp_text)
        return resp_text


    def _build_skill_string(self, input: str) -> str:
        skills = json.loads(input)
        output = ""
        for skill in skills[:5]:
            string = f"{skill['skill_name'].lower()} of proficiency {skill['skill_level'].lower()}, "
            output += string
        return output


    def _build_credits_string(self, input: str) -> str:
        credits = json.loads(input)
        output = ""
        for credit in credits[:5]:
            string = f"a {credit['credit_type']} with the title {credit['credit_title']} casted by the director {credit['credit_director']} where the profile held the role {credit['credit_role']}, "
            output += string
        return output


    def _create_embedding(self, input: str, type: str) -> List:
        if type == 'document':
            embedding = self.embeddings.embed_documents(texts=[input])[0]
        elif type == 'query':  
            embedding = self.embeddings.embed_query(text=input)
        else:
            raise Exception('Invalid embedding type. Choose `query` or `document`.')
        return embedding


class ModelFactory:
    def get_model(model_name: str, model_kwargs: str):
        if model_name == "bedrock/aws-titan":
            return BedrockEmbeddings(
                model_id="amazon.titan-embed-text-v1",
                client=boto3.client(
                    service_name='bedrock-runtime',
                    region_name=os.environ.get('AWS_REGION')  
                ),
                model_kwargs=ast.literal_eval(model_kwargs)
            )
        elif model_name == "bedrock/cohere-embed-english":
            return BedrockEmbeddings(
                model_id="cohere.embed-english-v3",
                client=boto3.client(
                    service_name='bedrock-runtime',
                    region_name=os.environ.get('AWS_REGION')
                ),
                model_kwargs={}
                
            )   
        elif model_name == "openai/text-embedding":
            return OpenAIEmbeddings(
                model="text-embedding-3-large",
                api_key=os.environ.get('OPENAI_API_KEY'),
                model_kwargs={}
            )
        else:
            raise Exception('Invalid embedding model name. Valid values are: `bedrock/aws-titan`, `openai/text-embedding`') 



# if __name__ == '__main__':
#     from api.common.logging import PythonLogger
#     logger = PythonLogger.get_logger("test")
#     embeddings_client = EmbeddingClient(
#         logger=logger,
#         model=None,
#         no_profiles=10
#     )

#     embeddings_client._create_vectors()