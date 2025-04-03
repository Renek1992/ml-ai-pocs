"""
Provides clients for AWS secrets manager.
"""

from boto3.session import Session
from mypy_boto3_s3.client import S3Client
from mypy_boto3_rekognition.client import RekognitionClient



class AwsS3Client:
    def __init__(self) -> None:
        session = Session()
        self.client: S3Client = session.client(service_name="s3")


class AwsRekognitionClient:
    def __init__(self) -> None:
        session = Session()
        self.client: RekognitionClient = session.client(service_name="rekognition")