from typing import Dict, Any
import trimesh
from strategies.organic_model import OrganicModelStrategy
from .base_object import BaseObject

class OrganicObject(BaseObject):
    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.strategy = OrganicModelStrategy()
        self.mesh = None

    def build(self) -> None:
        self.strategy.build_model(self.parameters)
        self.mesh = self.strategy.get_mesh()

    def get_mesh(self) -> trimesh.Trimesh:
        if self.mesh is None:
            self.build()
        return self.mesh
