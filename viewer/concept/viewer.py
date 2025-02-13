#!/usr/bin/env python3
"""
3D Renderer using Vispy and trimesh.

This module provides a simple 3D renderer that loads a 3D model and displays it
with interactive orbit controls.
"""

import sys
import trimesh
from vispy import app, scene
from pydantic import BaseModel, FilePath, ValidationError  # type: ignore


class ViewerConfig(BaseModel):
    """
    Configuration to be passed into the viewer
    """

    file_path: FilePath


def load_mesh(file_path: str) -> trimesh.Trimesh:
    """
    Load a mesh from the specified file path.

    If the file contains a Scene (i.e. multiple meshes), the geometries are
    concatenated into a single mesh.
    """

    mesh = trimesh.load(file_path)
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
    return mesh


def main(file_path: str) -> None:
    """
    Set up and run the 3D viewer with the provided 3D model.

    Loads the mesh, creates a Vispy canvas with an interactive view,
    adds the mesh visual, sets up a turntable camera for orbit controls, and runs
    the application.
    """
    mesh = load_mesh(file_path)
    vertices = mesh.vertices
    faces = mesh.faces

    canvas = scene.SceneCanvas(keys="interactive", show=True, bgcolor="black")
    view = canvas.central_widget.add_view()
    mesh_visual = scene.visuals.Mesh(
        vertices=vertices, faces=faces, color=(0.5, 0.5, 1, 1), shading="smooth"
    )
    view.add(mesh_visual)

    view.camera = scene.TurntableCamera(fov=45, distance=mesh.extents.max() * 2)
    view.camera.center = mesh.centroid

    _axis = scene.visuals.XYZAxis(parent=view.scene)
    app.run()


if __name__ == "__main__":
    app.use_app("PyQt5")

    if len(sys.argv) < 2:
        print("Usage: python viewer.py path/to/your_model.stl")
        sys.exit(1)

    try:
        config = ViewerConfig(file_path=sys.argv[1])
    except ValidationError as err:
        print("Configuration error:", err)
        sys.exit(1)

    main(str(config.file_path))
