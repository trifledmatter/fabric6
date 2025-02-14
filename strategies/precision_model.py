from typing import Dict, Any
import trimesh
import numpy as np
import cadquery as cq
from .modeling_strategy import ModelingStrategy


class PrecisionModelStrategy(ModelingStrategy):
    def __init__(self) -> None:
        self.model = None

    def build_model(self, parameters: Dict[str, Any]) -> None:
        length = parameters.get("length", 10)
        width = parameters.get("width", 10)
        height = parameters.get("height", 10)
        self.model = cq.Workplane("XY").box(length, width, height)

    def get_model(self):
        if self.model is None:
            raise ValueError("The precision model has not been built yet.")
        return self.model

    def get_mesh(self):
        if self.model is None:
            raise ValueError("The precision model has not been built yet.")
        tessellation = self.model.val().tessellate(0.55, 0.55)
        vertices, faces = tessellation
        try:
            vertices = np.array(
                [[float(v.x), float(v.y), float(v.z)] for v in vertices]
            )
        except AttributeError:
            vertices = np.array(vertices, dtype=float)
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
