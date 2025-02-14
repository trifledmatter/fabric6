import numpy as np
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QToolBar,
    QFileDialog,
    QMessageBox,
    QColorDialog,
    QMenuBar,
)
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtCore import QTimer
from vispy import scene, gloo
from vispy.scene.visuals import XYZAxis, Mesh
import trimesh
import imageio
from .config import ViewerConfig


def safe_slot(fn):
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An error occurred in {fn.__name__}:\n{e}"
            )

    return wrapper


class ViewerWindow(QMainWindow):
    def __init__(self, mesh: trimesh.Trimesh, config: ViewerConfig):
        super().__init__()
        self.config = config
        self.mesh = mesh
        self.quality = getattr(self.config, "quality", 12)
        self.autopan_enabled = True
        self.autopan_speed = 0.30
        self.user_interacting = False
        self.environment_light = {
            "color": (1, 1, 1, 1),
            "intensity": 1.0,
            "ambient": 0.3,
            "direction": (0, 0, -1),
            "specular": 0.5,
            "shininess": 32.0,
        }
        self.autopan_timer = QTimer(self)
        self.autopan_timer.setInterval(20)
        self.autopan_timer.timeout.connect(self.autopan_step)
        self.autopan_action = QAction("Autopan", self)
        self.autopan_action.setCheckable(True)
        self.autopan_action.toggled.connect(self.toggle_autopan)
        self.autopan_action.setChecked(True)
        self.init_canvas()
        self.create_menu()
        self.create_toolbar()
        self.apply_styles()

    def init_canvas(self):
        fmt = QSurfaceFormat()
        fmt.setSamples(self.quality)
        QSurfaceFormat.setDefaultFormat(fmt)
        self.canvas = scene.SceneCanvas(
            keys="interactive", show=True, bgcolor=self.config.background_color
        )
        self.canvas.create_native()
        self.canvas.native.setMinimumSize(
            self.config.window_width, self.config.window_height
        )
        self.setCentralWidget(self.canvas.native)
        self.setWindowTitle(f"{self.config.model_dump()['file_path']}")
        self.view = self.canvas.central_widget.add_view()
        if not hasattr(self.mesh, "vertex_normals") or self.mesh.vertex_normals is None:
            self.mesh.vertex_normals = self.mesh.compute_vertex_normals()
        vertices = np.array(self.mesh.vertices, dtype=np.float32)
        faces = np.array(self.mesh.faces)
        self.mesh_visual = Mesh(
            vertices=vertices,
            faces=faces,
            color=(0.5, 0.5, 1, 1),
        )
        self.view.add(self.mesh_visual)
        self.border_mesh = self.create_border_mesh(vertices, faces, scale=1.02)
        self.border_mesh.visible = False
        self.view.add(self.border_mesh)
        min_distance = 2.0
        computed_distance = self.mesh.extents.max() * 5
        self.view.camera = scene.TurntableCamera(
            fov=self.config.fov, distance=max(computed_distance, min_distance)
        )
        self.view.camera.center = self.mesh.centroid
        self.axis = XYZAxis(parent=self.view.scene)
        self.canvas.events.mouse_press.connect(self.on_mouse_press)
        self.canvas.events.mouse_release.connect(self.on_mouse_release)
        self.update_lighting()

    def update_lighting(self):
        try:
            self.mesh_visual.shared_program["u_ambient"] = self.environment_light.get(
                "ambient", 0.3
            )
            self.mesh_visual.shared_program["u_light_color"] = (
                self.environment_light.get("color", (1, 1, 1, 1))
            )
            self.mesh_visual.shared_program["u_light_intensity"] = (
                self.environment_light.get("intensity", 1.0)
            )
            self.mesh_visual.shared_program["u_light_direction"] = (
                self.environment_light.get("direction", (0, 0, -1))
            )
            self.mesh_visual.shared_program["u_specular"] = self.environment_light.get(
                "specular", 0.5
            )
            self.mesh_visual.shared_program["u_shininess"] = self.environment_light.get(
                "shininess", 32.0
            )
        except Exception:
            pass

    def create_border_mesh(self, vertices, faces, scale=1.02):
        border_vertices = vertices * scale
        border_mesh = Mesh(
            vertices=border_vertices,
            faces=faces,
            color=(0, 0, 0, 1),
            mode="lines",
        )
        border_mesh.set_gl_state(depth_test=False)
        border_mesh.order = 10
        return border_mesh

    def recreate_canvas(self):
        camera_center = self.view.camera.center
        camera_distance = self.view.camera.distance
        camera_fov = self.view.camera.fov
        self.canvas.close()
        self.init_canvas()
        self.view.camera.center = camera_center
        self.view.camera.distance = camera_distance
        self.view.camera.fov = camera_fov

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toggle_axis_action = QAction("Toggle Axis", self)
        toggle_axis_action.triggered.connect(self.toggle_axis)
        toolbar.addAction(toggle_axis_action)
        change_bg_action = QAction("Change Background", self)
        change_bg_action.triggered.connect(self.change_background_color)
        toolbar.addAction(change_bg_action)
        change_model_color_action = QAction("Change Model Color", self)
        change_model_color_action.triggered.connect(self.change_model_color)
        toolbar.addAction(change_model_color_action)
        toolbar.addAction(self.autopan_action)
        set_autopan_speed_action = QAction("Set Autopan Speed", self)
        set_autopan_speed_action.triggered.connect(self.set_autopan_speed)
        toolbar.addAction(set_autopan_speed_action)
        inc_quality_action = QAction("Increase Quality", self)
        inc_quality_action.triggered.connect(self.increase_quality)
        toolbar.addAction(inc_quality_action)
        dec_quality_action = QAction("Decrease Quality", self)
        dec_quality_action.triggered.connect(self.decrease_quality)
        toolbar.addAction(dec_quality_action)
        toggle_outline_action = QAction("Toggle Outline", self)
        toggle_outline_action.setCheckable(True)
        toggle_outline_action.toggled.connect(self.toggle_border)
        toolbar.addAction(toggle_outline_action)
        screenshot_action = QAction("Save Screenshot", self)
        screenshot_action.triggered.connect(self.save_screenshot)
        toolbar.addAction(screenshot_action)
        reload_action = QAction("Reload Mesh", self)
        reload_action.triggered.connect(self.reload_mesh)
        toolbar.addAction(reload_action)
        configure_env_light_action = QAction("Configure Environment Light", self)
        configure_env_light_action.triggered.connect(self.configure_environment_light)
        toolbar.addAction(configure_env_light_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

    def create_menu(self):
        menu_bar: QMenuBar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open Mesh", self)
        open_action.triggered.connect(self.reload_mesh)
        file_menu.addAction(open_action)
        save_action = QAction("Save Screenshot", self)
        save_action.triggered.connect(self.save_screenshot)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        view_menu = menu_bar.addMenu("View")
        toggle_axis_action = QAction("Toggle Axis", self)
        toggle_axis_action.triggered.connect(self.toggle_axis)
        view_menu.addAction(toggle_axis_action)
        change_bg_action = QAction("Change Background", self)
        change_bg_action.triggered.connect(self.change_background_color)
        view_menu.addAction(change_bg_action)
        change_model_color_action = QAction("Change Model Color", self)
        change_model_color_action.triggered.connect(self.change_model_color)
        view_menu.addAction(change_model_color_action)
        view_menu.addAction(self.autopan_action)
        set_autopan_speed_action = QAction("Set Autopan Speed", self)
        set_autopan_speed_action.triggered.connect(self.set_autopan_speed)
        view_menu.addAction(set_autopan_speed_action)
        quality_menu = view_menu.addMenu("Quality")
        inc_quality_menu_action = QAction("Increase Quality", self)
        inc_quality_menu_action.triggered.connect(self.increase_quality)
        quality_menu.addAction(inc_quality_menu_action)
        dec_quality_menu_action = QAction("Decrease Quality", self)
        dec_quality_menu_action.triggered.connect(self.decrease_quality)
        quality_menu.addAction(dec_quality_menu_action)
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        lighting_menu = menu_bar.addMenu("Lighting")
        configure_env_light_menu_action = QAction("Configure Environment Light", self)
        configure_env_light_menu_action.triggered.connect(
            self.configure_environment_light
        )
        lighting_menu.addAction(configure_env_light_menu_action)

    @safe_slot
    def toggle_border(self, enabled):
        self.border_mesh.visible = enabled
        self.canvas.update()

    def apply_styles(self):
        style_sheet = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QToolBar {
            background-color: #3c3f41;
            spacing: 10px;
            padding: 5px;
        }
        QToolBar QToolButton {
            background-color: #3c3f41;
            border: 1px solid #4e5254;
            border-radius: 4px;
            margin: 5px;
            padding: 8px 12px;
            color: #ffffff;
        }
        QToolBar QToolButton:hover {
            background-color: #4e5254;
        }
        QMenuBar {
            background-color: #3c3f41;
            color: #ffffff;
            padding: 5px;
        }
        QMenuBar::item {
            background-color: #3c3f41;
            padding: 4px 10px;
            margin: 2px;
        }
        QMenuBar::item:selected {
            background-color: #4e5254;
        }
        QMenu {
            background-color: #3c3f41;
            color: #ffffff;
            padding: 5px;
        }
        QMenu::item {
            padding: 4px 10px;
            margin: 2px;
        }
        QMenu::item:selected {
            background-color: #4e5254;
        }
        QMessageBox {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        """
        self.setStyleSheet(style_sheet)

    @safe_slot
    def show_about(self, *args, **kwargs):
        QMessageBox.information(
            self,
            "About",
            "3D Viewer\n\nA simple 3D model viewer built with Vispy and PyQt5.\n\nImproved environment lighting with specular highlights is provided via a custom shader.",
        )

    @safe_slot
    def toggle_axis(self, *args, **kwargs):
        if self.axis.parent is None:
            self.axis.parent = self.view.scene
        else:
            self.axis.parent = None
        self.canvas.update()

    @safe_slot
    def change_background_color(self, *args, **kwargs):
        color = QColorDialog.getColor()
        if color.isValid():
            new_color = color.name()
            self.config.background_color = new_color
            self.canvas.bgcolor = new_color
            self.canvas.update()

    @safe_slot
    def change_model_color(self, *args, **kwargs):
        color = QColorDialog.getColor()
        if color.isValid():
            new_color = color.getRgbF()
            self.mesh_visual.color = new_color
            self.canvas.update()

    @safe_slot
    def toggle_autopan(self, enabled, *args, **kwargs):
        self.autopan_enabled = enabled
        if enabled and not self.user_interacting:
            self.autopan_timer.start()
        else:
            self.autopan_timer.stop()

    @safe_slot
    def set_autopan_speed(self, *args, **kwargs):
        speed, ok = QInputDialog.getDouble(
            self,
            "Set Autopan Speed",
            "Degrees per step:",
            self.autopan_speed,
            -360,
            360,
            2,
        )
        if ok:
            self.autopan_speed = speed

    @safe_slot
    def autopan_step(self, *args, **kwargs):
        self.view.camera.azimuth += self.autopan_speed
        self.canvas.update()

    def on_mouse_press(self, event):
        if event.button == 1 and self.autopan_timer.isActive():
            self.autopan_timer.stop()
            self.user_interacting = True

    def on_mouse_release(self, event):
        if event.button == 1 and self.user_interacting and self.autopan_enabled:
            self.autopan_timer.start()
            self.user_interacting = False

    @safe_slot
    def increase_quality(self, *args, **kwargs):
        if self.quality < 16:
            self.quality += 1
            self.recreate_canvas()
            QMessageBox.information(
                self, "Quality Updated", f"Quality increased to {self.quality} samples."
            )

    @safe_slot
    def decrease_quality(self, *args, **kwargs):
        if self.quality > 0:
            self.quality -= 1
            self.recreate_canvas()
            QMessageBox.information(
                self, "Quality Updated", f"Quality decreased to {self.quality} samples."
            )

    @safe_slot
    def save_screenshot(self, *args, **kwargs):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "", "PNG Files (*.png);;All Files (*)"
        )
        if filename:
            img = self.canvas.render()
            try:
                imageio.imwrite(filename, img)
                QMessageBox.information(
                    self, "Screenshot", "Screenshot saved successfully."
                )
            except Exception as error:
                QMessageBox.critical(
                    self, "Error", f"Failed to save screenshot:\n{error}"
                )

    @safe_slot
    def reload_mesh(self, *args, **kwargs):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open 3D Model",
            "",
            "3D Model Files (*.stl *.obj *.ply *.off);;All Files (*)",
        )
        if filename:
            new_mesh = trimesh.load(filename)
            if isinstance(new_mesh, trimesh.Scene):
                new_mesh = trimesh.util.concatenate(list(new_mesh.geometry.values()))
            self.mesh = new_mesh
            self.mesh_visual.set_data(vertices=new_mesh.vertices, faces=new_mesh.faces)
            self.view.camera.center = new_mesh.centroid
            self.view.camera.distance = new_mesh.extents.max() * 2
            vertices = np.array(new_mesh.vertices, dtype=np.float32)
            faces = np.array(new_mesh.faces)
            self.border_mesh = self.create_border_mesh(vertices, faces, scale=1.02)
            self.border_mesh.visible = False
            self.view.add(self.border_mesh)
            self.canvas.update()

    @safe_slot
    def configure_environment_light(self, *args, **kwargs):
        ambient, ok = QInputDialog.getDouble(
            self,
            "Set Ambient Light",
            "Ambient Light (0-1):",
            self.environment_light["ambient"],
            0,
            1,
            2,
        )
        if ok:
            self.environment_light["ambient"] = ambient
        intensity, ok = QInputDialog.getDouble(
            self,
            "Set Light Intensity",
            "Intensity:",
            self.environment_light["intensity"],
            0,
            10,
            2,
        )
        if ok:
            self.environment_light["intensity"] = intensity
        specular, ok = QInputDialog.getDouble(
            self,
            "Set Specular Strength",
            "Specular (0-1):",
            self.environment_light.get("specular", 0.5),
            0,
            1,
            2,
        )
        if ok:
            self.environment_light["specular"] = specular
        shininess, ok = QInputDialog.getDouble(
            self,
            "Set Shininess",
            "Shininess (1-128):",
            self.environment_light.get("shininess", 32.0),
            1,
            128,
            0,
        )
        if ok:
            self.environment_light["shininess"] = shininess
        color = QColorDialog.getColor()
        if color.isValid():
            new_color = color.getRgbF()
            self.environment_light["color"] = new_color
        self.update_lighting()
        self.canvas.update()
