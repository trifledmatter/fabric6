from typing import List
from objects.base_object import BaseObject
from exporters.stl_exporter import STLExporter

class Scene:
    def __init__(self, mode: str = "precision") -> None:
        if mode not in ("organic", "precision"):
            raise ValueError("Mode must be 'organic' or 'precision'")
        self.mode = mode
        self.objects: List[BaseObject] = []

    def add(self, obj: BaseObject) -> None:
        self.objects.append(obj)

    def remove(self, obj: BaseObject) -> None:
        self.objects.remove(obj)

    def export_stl(self, filename: str) -> None:
        exporter = STLExporter()
        meshes = [obj.get_mesh() for obj in self.objects]
        combined_mesh = exporter.combine_meshes(meshes)
        exporter.export(combined_mesh, filename)
