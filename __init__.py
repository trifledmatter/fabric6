"""
py3dmodel: A Python library for code-based 3D modeling and STL export.

This library supports creating a Scene with objects that can be manipulated
and then exported as an STL file suitable for 3D printing. It offers a hybrid
approach with two modeling strategies: organic (using Trimesh) and precision
(using CadQuery).
"""

from .scene import Scene
from .objects import BaseObject, OrganicObject, PrecisionObject
from .exporters.stl_exporter import STLExporter

__all__ = ["Scene", "BaseObject", "OrganicObject", "PrecisionObject", "STLExporter"]
