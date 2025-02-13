"""
Module for managing 3D scenes.

A Scene contains objects and, upon export, combines their meshes into a single STL file.
"""

from typing import List
from objects.base_object import BaseObject
from exporters.stl_exporter import STLExporter


class Scene:
    """
    Represents a 3D scene.
    """

    def __init__(self, mode: str = "precision") -> None:
        """
        Initialize a Scene.

        :param mode: 'organic' or 'precision'
        """
        if mode not in ("organic", "precision"):
            raise ValueError("Mode must be 'organic' or 'precision'")
        self.mode = mode
        self.objects: List[BaseObject] = []

    def add(self, obj: BaseObject) -> None:
        """
        Add an object to the scene.

        :param obj: Instance of BaseObject.
        """
        self.objects.append(obj)

    def remove(self, obj: BaseObject) -> None:
        """
        Remove an object from the scene.

        :param obj: Instance of BaseObject.
        """
        self.objects.remove(obj)

    def export_stl(self, filename: str) -> None:
        """
        Combine all objects in the scene and export them as an STL file.

        :param filename: Output file path.
        """
        exporter = STLExporter()
        # Each object returns its mesh (a trimesh.Trimesh instance)
        meshes = [obj.get_mesh() for obj in self.objects]
        combined_mesh = exporter.combine_meshes(meshes)
        exporter.export(combined_mesh, filename)
