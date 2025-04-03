

from typing import Dict
from logging import Logger

from shared.aws.aws_clients import AwsRekognitionClient
from shared.aws.aws_operations import (
    rekogn__create_project,
    rekogn__create_dataset
)


class RekognitionProjectSetup:
    def __init__(self, manifest_location: Dict) -> None:
        self.rekogn_client = AwsRekognitionClient()
        self.manifest_location = manifest_location


    def setup_project(self, logger: Logger): 
        project_arn = rekogn__create_project(
            logger=logger, 
            rekogn_client=self.rekogn_client,
            project_name = "devActorSimilarity"    
        )
        dataset_arn = rekogn__create_dataset(
            logger=logger,
            rekogn_client=self.rekogn_client,
            project_arn=project_arn,
            dataset_type='TRAIN',
            manifest_location=self.manifest_location
        )
