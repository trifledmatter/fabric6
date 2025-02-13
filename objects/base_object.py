"""
Abstract base class for 3D objects in the scene.
"""

from typing import Dict, Any


class BaseObject:
    """
    Abstract base class for objects.
    """

    def __init__(self, parameters: Dict[str, Any] = None) -> None:
        """
        Initialize the object.

        :param parameters: Dictionary of parameters.
        """
        self.parameters = parameters if parameters is not None else {}

    def build(self) -> None:
        """
        Build the 3D model. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement build()")

    def manipulate(self, **kwargs) -> None:
        """
        Manipulate the object by updating parameters and rebuilding the model.

        :param kwargs: Parameters to update.
        """
        self.parameters.update(kwargs)
        self.build()

    def get_mesh(self):
        """
        Return the mesh representation of the object.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement get_mesh()")
