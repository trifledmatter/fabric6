# pylint: disable=no-name-in-module,import-error,missing-module-docstring,missing-class-docstring

from pydantic import BaseModel, FilePath


class ViewerConfig(BaseModel):
    file_path: FilePath
    background_color: str = "black"
    window_width: int = 800
    window_height: int = 600
    fov: float = 45.0
