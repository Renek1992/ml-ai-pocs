"""
Main runner for image comparsion (s3)
"""
import os
import boto3
import json
import hashlib
from typing import List
from datetime import datetime
from shared.telemetry.logs.logging import PythonLogger
from shared.aws.aws_clients import AwsRekognitionClient
from shared.aws.aws_operations import rekogn__compare_faces__s3, rekogn__detect_faces__s3
from shared.db.snowflake_handler import SnowflakeHandler


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


profile_images: List = get_file_names(prefix='celebrity-profiles/')


logger = PythonLogger.get_logger(name='facial-analysis', log_level='DEBUG')



def run():
    rekogn_client = AwsRekognitionClient()
    snowflake_handler = SnowflakeHandler(
        logger=logger, 
        table_name=os.environ.get('SF_TABLE')
    )
    


    for profile in profile_images[1:]:
        
        resp = rekogn__detect_faces__s3(
            logger=logger,
            rekogn_client=rekogn_client,
            bucket_name=BUCKET_NAME,
            image_key=profile
        )
        # print(resp)
        # for item in resp['FaceDetails']:
        #     print('AgeRange', item['AgeRange'])
        #     print('Beard', item['Beard'])
        #     print('Mustache', item['Mustache'])
        #     print('Gender', item['Gender'])
        #     print('Emotions', item['Emotions'])
        # print('----------------------------')
        
        emotions = []
        if len(resp['FaceDetails'][0]['Emotions']) > 0:
            for emotion in resp['FaceDetails'][0]['Emotions']:
                if emotion['Confidence'] > 80.0:
                    emotions.append(emotion['Type'].lower())

        age_range = {'low_age': resp['FaceDetails'][0]['AgeRange']['Low'], 'high_age': resp['FaceDetails'][0]['AgeRange']['High']}

        log_id = hashlib.md5((profile).encode())

        results = {
            'id' : log_id.hexdigest(),
            'profile_location' : profile,
            'age_range' : age_range,
            'gender' : str(resp['FaceDetails'][0]['Gender']['Value'].lower()),
            'emotions' : emotions,
            'generated_on' : str(datetime.now()),
            'raw_payload' : json.dumps(resp, default=str)
        }
        try:
            snowflake_handler.insert_data(result=results)
        except Exception as e:
            logger.error(f'error: {e} // result_log: {results}')
            





if __name__ == '__main__':
    run()
