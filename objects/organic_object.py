"""
Organic object implementation using Trimesh.
"""

from typing import Dict, Any
import trimesh
from strategies.organic_model import OrganicModelStrategy

from .base_object import BaseObject


class OrganicObject(BaseObject):
    """
    Represents an organic, freeform object.
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.strategy = OrganicModelStrategy()
        self.mesh = None

    def build(self) -> None:
        """
        Build the organic model.
        """
        self.strategy.build_model(self.parameters)
        self.mesh = self.strategy.get_mesh()

    def get_mesh(self) -> trimesh.Trimesh:
        """
        Return the trimesh representation of the object.
        """
        if self.mesh is None:
            self.build()
        return self.mesh
