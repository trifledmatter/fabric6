# main.py
# pylint: disable=missing-function-docstring,missing-module-docstring
from scene import Scene
from viewer.main import main as render_obj
from objects.primitives import Cube, Sphere, Pyramid, Cylinder


def main() -> None:
    """
    Example usage of the library, i've made a man :)
    """
    scene_obj = Scene(mode="precision")

    torso_params = {"length": 15, "width": 10, "height": 20}
    torso_obj = Cube(parameters=torso_params)
    torso_obj.build()
    torso_obj.model = torso_obj.model.translate((0, 0, 10))
    scene_obj.add(torso_obj)

    head_params = {"radius": 5}
    head_obj = Sphere(parameters=head_params)
    head_obj.build()
    head_obj.model = head_obj.model.translate((0, 0, 23))
    scene_obj.add(head_obj)

    arm_params = {"height": 18, "radius": 2}
    left_arm_obj = Cylinder(parameters=arm_params)
    left_arm_obj.build()
    left_arm_obj.model = left_arm_obj.model.rotateAboutCenter((0, 0, 1), 90).translate(
        (-9, 0, 18)
    )
    scene_obj.add(left_arm_obj)

    right_arm_obj = Cylinder(parameters=arm_params)
    right_arm_obj.build()
    right_arm_obj.model = right_arm_obj.model.rotateAboutCenter(
        (0, 0, 1), -90
    ).translate((9, 0, 18))
    scene_obj.add(right_arm_obj)

    leg_params = {"height": 22, "radius": 2.5}
    left_leg_obj = Cylinder(parameters=leg_params)
    left_leg_obj.build()
    left_leg_obj.model = left_leg_obj.model.translate((-4, 0, -1))
    scene_obj.add(left_leg_obj)

    right_leg_obj = Cylinder(parameters=leg_params)
    right_leg_obj.build()
    right_leg_obj.model = right_leg_obj.model.translate((4, 0, -1))
    scene_obj.add(right_leg_obj)

    foot_params = {"base": 6, "height": 2}
    left_foot_obj = Pyramid(parameters=foot_params)
    left_foot_obj.build()
    left_foot_obj.model = left_foot_obj.model.translate((-4, 0, -12))
    scene_obj.add(left_foot_obj)

    right_foot_obj = Pyramid(parameters=foot_params)
    right_foot_obj.build()
    right_foot_obj.model = right_foot_obj.model.translate((4, 0, -12))
    scene_obj.add(right_foot_obj)

    output_file = "./target/model.stl"
    scene_obj.export_stl(output_file)
    print(f"Scene exported to {output_file}")

    render_obj()


if __name__ == "__main__":
    main()
