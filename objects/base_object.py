"""
Abstract base class for 3D objects in the scene.
"""

from typing import Dict, Any


class BaseObject:

    def __init__(self, parameters: Dict[str, Any] = None) -> None:

        self.parameters = parameters if parameters is not None else {}

    def build(self) -> None:
        raise NotImplementedError("Subclasses must implement build()")

    def manipulate(self, **kwargs) -> None:
        self.parameters.update(kwargs)
        self.build()

    def get_mesh(self):
        raise NotImplementedError("Subclasses must implement get_mesh()")
