"""
Precision modeling strategy using CadQuery.
"""

from typing import Dict, Any

import trimesh
import numpy as np
import cadquery as cq

from .modeling_strategy import ModelingStrategy


class PrecisionModelStrategy(ModelingStrategy):
    """
    Implements a precise, parametric modeling approach with CadQuery.
    """

    def __init__(self) -> None:
        self.model = None

    def build_model(self, parameters: Dict[str, Any]) -> None:
        """
        Build the precision model using CadQuery.

        For demonstration, this creates a box.

        :param parameters: Dictionary with keys 'length', 'width', and 'height'
        """
        length = parameters.get("length", 10)
        width = parameters.get("width", 10)
        height = parameters.get("height", 10)
        self.model = cq.Workplane("XY").box(length, width, height)

    def get_model(self):
        """
        Return the CadQuery model.

        :return: The built CadQuery solid.
        """
        if self.model is None:
            raise ValueError("The precision model has not been built yet.")
        return self.model

    def get_mesh(self):
        """
        Return the mesh representation of the CadQuery model.

        This method tessellates the solid and converts the resulting vertices and faces
        into a trimesh.Trimesh object, which can then be exported as STL.

        :return: A trimesh.Trimesh object representing the model.
        """
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
