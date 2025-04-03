"""
Creator for manifest file
"""
import os
import json
import time
import pprint as pp
from typing import List, Dict
from logging import Logger
from datetime import datetime, timezone 
from shared.aws.aws_operations import s3__get_files, s3__upload_file
from shared.aws.aws_clients import AwsS3Client

class ManifestCreator:
    def __init__(self, bucket_name: str) -> None:
        self.s3_client = AwsS3Client()
        self.bucket_name = bucket_name

    
    def get_image_file_locations(self, logger: Logger):
        results = s3__get_files(logger=logger, s3_client=self.s3_client, bucket_name=self.bucket_name)
        filtered_results = []
        suffixes = (".jpeg", ".jpg", ".png")
        for item in results:
            if item['Key'].endswith(suffixes):
                filtered_results.append(item['Key'])
        # pp.pprint(filtered_results)
        logger.info("Successfully retrieved files from S3.")
        return filtered_results

    
    def get_image_labels(self, logger: Logger, file_list: List) -> List[Dict]:
        results  = []
        for file in file_list:
            db, name, file_name = file.split("/")
            gender = db.split("-")[0]
            year = file_name.split("-")[0]
            resp_dict = {
                "File_Name" : self.bucket_name + "/" + file,
                "File_Labels": [gender, name, year]
            }
            results.append(resp_dict)
        logger.info("List with labels created.")
        # pp.pprint(results)
        return results


    def create_manifest_file(
            self, 
            logger: Logger, 
            source_file: str, 
            manifest_s3_file_path: str, 
            manifest_local_file_path: str
    ):
        """
        Reads a CSV file and creates a Custom Labels classification manifest file.
        :param csv_file: The source CSV file.
        :param manifest_file: The name of the manifest file to create.
        :param s3_path: The S3 path to the folder that contains the images.
        """
        file_path = manifest_local_file_path

        image_count = 0
        label_count = 0
        result = False 
        self._check_and_delete_file(logger=logger, file_path=file_path)

        with open(file_path, "w", encoding="UTF-8") as output_file:

            for file in source_file:
                json_line = {}
                json_line['source-ref'] = 's3://' + file['File_Name']

                for label in file['File_Labels']:
                    json_line[label] = 1
                    metadata = {}
                    metadata['confidence'] = 1
                    metadata['job-name'] = 'labeling-job/' + label
                    metadata['class-name'] = label
                    metadata['human-annotated'] = "yes"
                    metadata['creation-date'] = \
                        datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')
                    metadata['type'] = "groundtruth/image-classification"

                    json_line[f'{label}-metadata'] = metadata

                    label_count += 1

                image_count += 1
                logger.info(f'File: {json_line['source-ref']} processed.')
                output_file.write(json.dumps(json_line))
                output_file.write('\n')
                time.sleep(0.5)

        output_file.close()
        logger.info(f"Created manifest with {image_count} images and {label_count} labels.")

        # upload file to S3
        s3__upload_file(
            logger=logger, 
            s3_client=self.s3_client, 
            bucket_name=self.bucket_name,
            file_key=manifest_s3_file_path,
            local_file_key=manifest_local_file_path)
        logger.info(f"Uploaded manifest to Bucket: {self.bucket_name}")
        result = True
        return result
    

    def _check_and_delete_file(self, logger: Logger, file_path: str):
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                logger.info("Existing manifest file removed.")
            except Exception as e:
                raise e
        else:
            logger.info("No manifest exists.")
            




