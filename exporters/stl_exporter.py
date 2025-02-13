"""
Module to export mesh objects as STL files.
"""

from typing import List
import trimesh


class STLExporter:
    """
    Combines mesh objects and exports the resulting mesh as an STL file.
    """

    def combine_meshes(self, meshes: List[trimesh.Trimesh]) -> trimesh.Trimesh:
        """
        Combine a list of trimesh objects into one mesh.

        :param meshes: List of trimesh.Trimesh instances.
        :return: A combined trimesh.Trimesh.
        """
        if not meshes:
            raise ValueError("No meshes to combine.")
        return trimesh.util.concatenate(meshes)

    def export(self, mesh: trimesh.Trimesh, filename: str) -> None:
        """
        Export the mesh to an STL file.

        :param mesh: A trimesh.Trimesh instance.
        :param filename: Output file path.
        """
        mesh.export(filename, file_type="stl")
