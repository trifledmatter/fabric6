# pylint: disable=no-name-in-module,import-error,missing-module-docstring

import trimesh


def load_mesh(file_path: str) -> trimesh.Trimesh:
    mesh = trimesh.load(file_path)
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
    return mesh
