# pylint: disable="unnecessary-pass"
"""
Defines the interface for modeling strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ModelingStrategy(ABC):
    """
    Abstract base class for modeling strategies.
    """

    @abstractmethod
    def build_model(self, parameters: Dict[str, Any]) -> None:
        """
        Build the model based on given parameters.
        """
        pass

    @abstractmethod
    def get_mesh(self):
        """
        Return the mesh representation of the model.
        """
        pass
