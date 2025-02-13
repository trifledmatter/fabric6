# pylint: disable=no-name-in-module,import-error,missing-module-docstring,missing-function-docstring,broad-exception-caught

import sys
import traceback
from vispy import app
from pydantic import ValidationError

from PyQt5.QtWidgets import QApplication

from viewer.lib.config import ViewerConfig
from viewer.lib.mesh_loader import load_mesh
from viewer.lib.ui import ViewerWindow


def main():
    app.use_app("pyqt5")

    if len(sys.argv) < 2:
        sys.argv.append("./target/model.stl")

    try:
        config = ViewerConfig(file_path=sys.argv[1])
    except ValidationError as err:
        print("Configuration error:", err)
        sys.exit(1)

    try:
        mesh = load_mesh(str(config.file_path))
    except Exception as e:
        print(f"Failed to load mesh: {e}")
        sys.exit(1)
    qt_app = QApplication(sys.argv)

    window = ViewerWindow(mesh, config)
    window.show()

    try:
        qt_app.exec_()
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
