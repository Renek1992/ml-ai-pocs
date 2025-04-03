"""
Provides abstract base class for the manifest generator.
"""
from abc import ABC, abstractmethod
from typing import Dict


class ManifestGenerator(ABC):
    """
    Abstract base class for the manifest generator.
    """

    @abstractmethod
    def generate_manifest(self, **kwargs) -> Dict:
        """
        Generate the manifest file.

        :param kwargs: The keyword arguments.
        :return: The manifest file.
        """
        raise NotImplementedError()