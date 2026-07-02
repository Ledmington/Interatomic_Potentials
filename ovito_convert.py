import os

os.environ["OVITO_GUI_MODE"] = "1"

import sys

trajectory_file = sys.argv[1]

import PySide6.QtWidgets

app = PySide6.QtWidgets.QApplication()

print("usage: python3 ovito_render.py [trajectory_file]")

from ovito.io import import_file
from ovito.vis import *


def main():

    # Load LAMMPS trajectory
    pipeline = import_file(trajectory_file)
    pipeline.add_to_scene()

    vp = Viewport()
    vp.zoom_all()

    vp.render_anim(
        size=(800, 600),
        filename="output.mp4",
        fps=15,
        renderer=OpenGLRenderer(),
        range=(0, pipeline.source.num_frames),
    )


if __name__ == "__main__":
    main()
