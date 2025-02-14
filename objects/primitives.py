import cadquery as cq
import numpy as np
import trimesh
from typing import Dict, Any

from .base_object import BaseObject


class Cube(BaseObject):
    """
    Cube object.

    Parameters:
      - length: cube length (default 10)
      - width: cube width (default 10)
      - height: cube height (default 10)
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.model = None

    def build(self) -> None:
        length = self.parameters.get("length", 10)
        width = self.parameters.get("width", 10)
        height = self.parameters.get("height", 10)
        self.model = cq.Workplane("XY").box(length, width, height)

    def get_mesh(self):
        if self.model is None:
            self.build()
        tessellation = self.model.val().tessellate(0.1, 0.1)
        vertices, faces = tessellation
        try:
            vertices = np.array(
                [[float(v.x), float(v.y), float(v.z)] for v in vertices]
            )
        except AttributeError:
            vertices = np.array(vertices, dtype=float)
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)


class Sphere(BaseObject):
    """
    Sphere object.

    Parameters:
      - radius: sphere radius (default 5)
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.model = None

    def build(self) -> None:
        radius = self.parameters.get("radius", 5)
        self.model = cq.Workplane("XY").sphere(radius)

    def get_mesh(self):
        if self.model is None:
            self.build()
        tessellation = self.model.val().tessellate(0.1, 0.1)
        vertices, faces = tessellation
        try:
            vertices = np.array(
                [[float(v.x), float(v.y), float(v.z)] for v in vertices]
            )
        except AttributeError:
            vertices = np.array(vertices, dtype=float)
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)


class Cylinder(BaseObject):
    """
    Cylinder object.

    Parameters:
      - height: cylinder height (default 10)
      - radius: cylinder radius (default 3)
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.model = None

    def build(self) -> None:
        height = self.parameters.get("height", 10)
        radius = self.parameters.get("radius", 3)
        self.model = cq.Workplane("XY").cylinder(height, radius)

    def get_mesh(self):
        if self.model is None:
            self.build()
        tessellation = self.model.val().tessellate(0.1, 0.1)
        vertices, faces = tessellation
        try:
            vertices = np.array(
                [[float(v.x), float(v.y), float(v.z)] for v in vertices]
            )
        except AttributeError:
            vertices = np.array(vertices, dtype=float)
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)


class Pyramid(BaseObject):
    """
    Pyramid object with a square base.

    Parameters:
      - base: length of the square base (default 10)
      - height: pyramid height (default 15)
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        super().__init__(parameters)
        self.model = None

    def build(self) -> None:
        base = self.parameters.get("base", 10)
        height = self.parameters.get("height", 15)
        self.model = (
            cq.Workplane("XY")
            .rect(base, base)
            .workplane(offset=height)
            .rect(0.001, 0.001)
            .loft(ruled=True, combine=True)
        )

    def get_mesh(self):
        if self.model is None:
            self.build()
        tessellation = self.model.val().tessellate(0.1, 0.1)
        vertices, faces = tessellation
        try:
            vertices = np.array(
                [[float(v.x), float(v.y), float(v.z)] for v in vertices]
            )
        except AttributeError:
            vertices = np.array(vertices, dtype=float)
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
