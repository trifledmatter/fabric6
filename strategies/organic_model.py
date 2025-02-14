from typing import Dict, Any
import trimesh
import numpy as np
from .modeling_strategy import ModelingStrategy


class OrganicModelStrategy(ModelingStrategy):
    def __init__(self) -> None:
        self.mesh = None

    def build_model(self, parameters: Dict[str, Any]) -> None:
        radius = parameters.get("radius", 1.0)
        subdivisions = parameters.get("subdivisions", 3)
        noise_scale = parameters.get("noise_scale", 0.1)
        base_mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        noise = noise_scale * np.random.randn(*base_mesh.vertices.shape)
        base_mesh.vertices += noise
        self.mesh = base_mesh

    def get_mesh(self):
        if self.mesh is None:
            raise ValueError("The organic model has not been built yet.")
        return self.mesh
