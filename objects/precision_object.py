"""
Precision object implementation using CadQuery.
"""

from typing import Dict, Any
from strategies.precision_model import PrecisionModelStrategy

from .base_object import BaseObject


class PrecisionObject(BaseObject):
    """
    Represents a precise, parametric object.
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.strategy = PrecisionModelStrategy()
        self.model = None

    def build(self) -> None:
        """
        Build the precision model.
        """
        self.strategy.build_model(self.parameters)
        self.model = self.strategy.get_model()

    def get_mesh(self):
        """
        Return a mesh representation of the model.

        :return: A mesh object that can be exported via STLExporter.
        """
        if self.model is None:
            self.build()
        return self.strategy.get_mesh()
