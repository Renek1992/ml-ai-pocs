"""
Main runner for image comparsion (local)
"""
from typing import List
from shared.aws.aws_clients import AwsRekognitionClient
from shared.aws.aws_operations import rekogn__compare_faces__local, rekogn__detect_faces__local
from shared.telemetry.logs.logging import PythonLogger

from shared.common.utils import read_image_as_bytes, write_json_to_file
from shared.common.erros import InvalidCelebrityImage, InvalidProfileImage



# add image sources here
celebrity_images: List = [
    './data/celebrities/maybe-robert-deniro-1.jpeg'
]

profile_images: List = [
    './data/profiles/maybe-robert-deniro-1.jpeg'
]



logger = PythonLogger.get_logger(name='celebrity-comparsion', log_level='DEBUG')



def run() -> None:
    rekogn_client = AwsRekognitionClient()
    results = {"Results" : []}
    sim_threshold = 80.0

    for celebrity in celebrity_images:
        celebrity_bytes: bytes = read_image_as_bytes(celebrity)
        resp = rekogn__detect_faces__local(
            logger=logger, 
            rekogn_client=rekogn_client,
            image_bytes=celebrity_bytes
        )
        if len(resp['FaceDetails']) > 0:
            logger.info(f'Comparing images for: {celebrity} ...')
            for profile in profile_images:
                profile_bytes: bytes = read_image_as_bytes(profile)
                resp = rekogn__detect_faces__local(
                    logger=logger, 
                    rekogn_client=rekogn_client,
                    image_bytes=profile_bytes,
                )
                if len(resp['FaceDetails']) > 0:
                    resp = rekogn__compare_faces__local(
                        logger=logger,
                        rekogn_client=rekogn_client,
                        src_image_bytes=celebrity_bytes, 
                        trg_image_bytes=profile_bytes,
                        sim_threshold=sim_threshold
                    )
                    logger.info(f"Similarity between celebrity: {celebrity} and profile: {profile} is {resp['FaceMatches'][0]['Similarity']}")
                    logger.debug(resp)
                    result_log = {
                        "Celebrity" : celebrity,
                        "Profile" : profile,
                        "Similarity_Score" : resp['FaceMatches'][0]['Similarity'],
                        "Similarity_Threshold" : sim_threshold
                    }
                    results['Results'].append(result_log)
                else:
                    err_msg = f"No face detected in profile image: {profile}"
                    logger.error(err_msg)
                    raise InvalidProfileImage(err_msg)
        else:
            err_msg = f"No face detectd in celebrity image: {celebrity}"
            logger.error(err_msg)
            raise InvalidCelebrityImage(err_msg)
    
    write_json_to_file(data=results, directory='./src/results/', filename='output.json')   




if __name__ == '__main__':
    run()