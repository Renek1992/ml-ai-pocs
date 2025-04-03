"""

"""
from logging import Logger
from typing import List, Dict
from deepface import DeepFace
from shared.telemetry.logs.logging import PythonLogger


celebrities_list: List = [
    "./data/celebrities/celeb4.png"
]

profiles_list: List = [
    "./data/profiles/actor4.png"
]

class FaceComparsion:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger


    def compare(self) -> Dict:
        for celeb in celebrities_list:
            for profile in profiles_list:
                result = DeepFace.verify(
                    img1_path= celeb,
                    img2_path= profile,
                    model_name="Facenet"
                )
                self.logger.info(f"Comparing: {celeb}")
                self.logger.info(f"To: {profile}")
                self.logger.info(f"Result: verified={result['verified']} | similarity={((1-result['distance'])*100):2f} | threshold={1-result['threshold']}")
                self.logger.info(f"Execution: time_in_sec={result['time']} | model={result['model']}")
                self.logger.info(f"----------------------------------------")



if __name__ == '__main__':
    logger = PythonLogger.get_logger(name='deepface_test', log_level='INFO')

    face_comparsion = FaceComparsion(logger=logger)
    face_comparsion.compare()
