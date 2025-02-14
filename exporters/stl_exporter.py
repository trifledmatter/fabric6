from typing import List
import trimesh


class STLExporter:

    def combine_meshes(self, meshes: List[trimesh.Trimesh]) -> trimesh.Trimesh:

        if not meshes:
            raise ValueError("No meshes to combine.")
        return trimesh.util.concatenate(meshes)

    def export(self, mesh: trimesh.Trimesh, filename: str) -> None:
        mesh.export(filename, file_type="stl")
