"""
Service that creates a manifest of db table schemas.
"""

from logging import Logger
from typing import Dict, Any


from manifest_generator_base import ManifestGeneratorBase



class ManifestGenerator(ManifestGeneratorBase):
    """ 
    Service that creates a manifest of celebrity profiles.
    """

    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)

    def generate_manifest(self) -> Dict[str, Any]:
        """
        Generate a manifest of celebrity profiles.
        """
        return {}