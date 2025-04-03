"""
main script
"""
from pipeline.data_pipeline import RekognitionProjectSetup
from manifest.manifest_generator import ManifestCreator
from shared.telemetry.logs.logging import PythonLogger
from shared.common.utils import interactive_sleep


logger = PythonLogger.get_logger(name='rekognition_data_pipeline')


MANIFEST_LOCAL_FILE_PATH = "data/manifest/manifest.manifest"
MANIFEST_S3_FILE_PATH = "manifest/manifest.manifest"
BUCKET_NAME = "dev-poc-actor-rekognition-281935296038-us-east-1"



def run():
    # build manifest
    manifest_generator = ManifestCreator(
        bucket_name=BUCKET_NAME
    )
    file_list = manifest_generator.get_image_file_locations(logger=logger)
    labeled_list = manifest_generator.get_image_labels(logger=logger, file_list=file_list)
    manifest_generator.create_manifest_file(
        logger=logger,
        source_file=labeled_list,
        manifest_local_file_path=MANIFEST_LOCAL_FILE_PATH,
        manifest_s3_file_path=MANIFEST_S3_FILE_PATH
    )
    
    interactive_sleep(15)


    # create location object
    manifest_location = {
        "Bucket" : BUCKET_NAME,
        "File_Key" : MANIFEST_S3_FILE_PATH
    }
    rekognition_project_setup = RekognitionProjectSetup(
        manifest_location=manifest_location
    )
    rekognition_project_setup.setup_project(logger=logger)





if __name__ == '__main__':
    run()