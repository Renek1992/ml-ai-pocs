"""
Main runner for image comparsion (s3)
"""
import os
import hashlib
import boto3
from datetime import datetime
from typing import List
from shared.aws.aws_clients import AwsRekognitionClient
from shared.aws.aws_operations import rekogn__compare_faces__s3, rekogn__detect_faces__s3
from shared.db.snowflake_handler import SnowflakeHandler
from shared.telemetry.logs.logging import PythonLogger

from shared.common.utils import write_json_to_file
from shared.common.erros import InvalidCelebrityImage, InvalidProfileImage

BUCKET_NAME = os.environ.get('BUCKET_NAME')



def get_file_names(prefix: str) -> List:
    file_list: List = []
    client = boto3.client('s3')
    resp = client.list_objects_v2(
        Bucket=os.environ.get('BUCKET_NAME'),
        Prefix=prefix
    )
    if len(resp['Contents']) > 0:
        for item in resp['Contents']:
            file_list.append(item['Key'])
    return file_list



# add image sources here
celebrity_images: List = get_file_names(prefix='celebrities/')

profile_images: List = get_file_names(prefix='celebrity-profiles/')



logger = PythonLogger.get_logger(name='celebrity-comparsion', log_level='DEBUG')


def run() -> None:
    rekogn_client = AwsRekognitionClient()
    snowflake_handler = SnowflakeHandler(
        logger=logger, 
        table_name=os.environ.get('SF_TABLE')
    )
    results = {"Results" : []}
    sim_threshold = 0.0

    for celebrity in celebrity_images[celebrity_images.index('celebrities/Steve_Aoki.jpg'):]:
        
        for profile in profile_images[1:]:
            logger.info(f'Comparing images for: {celebrity} and {profile} ...')
            resp = rekogn__compare_faces__s3(
                logger=logger,
                rekogn_client=rekogn_client,
                bucket_name=BUCKET_NAME,
                src_image_key=celebrity,
                trg_image_key=profile,
                sim_threshold=sim_threshold
            )
            logger.debug(resp)
            logger.info(f"Similarity between celebrity: {celebrity} and profile: {profile} is {resp['FaceMatches'][0]['Similarity']}")
            
            log_id = hashlib.md5((celebrity + profile).encode())
            result_log = {
                "Id" : log_id.hexdigest(),
                "Celebrity" : celebrity,
                "Profile" : profile,
                "Similarity_Score" : resp['FaceMatches'][0]['Similarity'],
                "Similarity_Threshold" : sim_threshold,
                "Generated_On" : str(datetime.now())
            }
            try:
                snowflake_handler.insert_data(result=result_log)
            except Exception as e:
                logger.error(f'error: {e} // result_log: {result_log}')
            results['Results'].append(result_log)


    write_json_to_file(data=results, directory='./src/results/', filename='output.json')   






if __name__ == '__main__':
    run()
