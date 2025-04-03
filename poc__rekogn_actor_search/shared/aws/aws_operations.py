"""
Provides a repository of aws operations utilizing AWS clients.
"""
from logging import Logger
from typing import List, Dict, Literal
from shared.aws.aws_clients import (
    AwsS3Client,
    AwsRekognitionClient
)
from botocore.exceptions import ClientError


def s3__get_files(logger: Logger, s3_client: AwsS3Client, bucket_name: str) -> List:
    try:
        resp = s3_client.client.list_objects_v2(
            Bucket=bucket_name,
        )
        return resp['Contents']
    except ClientError as e:
        logger.debug(f"bucket: {bucket_name}")
        logger.error(f"File upload failed: {e}")
        raise e


def s3__upload_file(logger: Logger, s3_client: AwsS3Client, bucket_name: str, file_key: str, local_file_key: str) -> bool:
    result = False
    try:
        resp = s3_client.client.upload_file(
            Bucket=bucket_name,
            Key=file_key, 
            Filename=local_file_key
        )
        if resp:
            result = True
    except ClientError as e:
        logger.debug(f"bucket: {bucket_name} // file_key: {file_key}")
        logger.error(f"File upload failed: {e}")
        raise e
    return result


def rekogn__create_project(logger: Logger, rekogn_client: AwsRekognitionClient, project_name: str) -> str:
    try:
        resp = rekogn_client.client.create_project(ProjectName=project_name)
        logger.info(f"Created new AWS Rekognition project with name: {project_name}")
        return resp["ProjectArn"]
    except ClientError as e:
        logger.error(f"Project creation for AWS Rekognition failed: {e}")
        raise e


def rekogn__create_dataset(logger: Logger, rekogn_client: AwsRekognitionClient, project_arn: str, dataset_type: Literal['TRAIN', 'TEST'], manifest_location: Dict[str, str]) -> str:
    try:
        resp = rekogn_client.client.create_dataset(
            DatasetType=dataset_type,
            ProjectArn=project_arn,
            DatasetSource={ 
                'GroundTruthManifest': { 
                    'S3Object': { 
                        'Bucket': manifest_location["Bucket"] , 
                        'Name': manifest_location["File_Key"] 
                    } 
                } 
            }
        )
        logger.info(f"Created new dataset for AWS Rekognition project: {project_arn}")
        return resp["DatasetArn"]
    except ClientError as e:
        logger.error(f"Dataset creation for AWS Rekognition failed: {e}")
        raise e
    

def rekogn__update_dataset_entries(logger: Logger, rekogn_client: AwsRekognitionClient, dataset_arn: str, change_json_line: Dict) -> Dict:
    try:
        resp = rekogn_client.client.update_dataset_entries(
            DatasetArn=dataset_arn, 
            Changes=change_json_line
        )
        logger.info("Dataset has been updated.")
        return resp
    except ClientError as e:
        logger.error(f"Update for dataset arn: {dataset_arn} failed.")
        raise e
