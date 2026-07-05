import os

os.environ["OVITO_GUI_MODE"] = "1"

import argparse
import PySide6.QtWidgets

from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render OVITO trajectory animations to video."
    )

    parser.add_argument(
        "trajectory", help="Input trajectory file (e.g. LAMMPS dump, .xyz, etc.)"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="output.mp4",
        help="Output video filename (default: output.mp4)",
    )

    parser.add_argument(
        "--width", type=int, default=800, help="Render width in pixels (default: 800)"
    )

    parser.add_argument(
        "--height", type=int, default=600, help="Render height in pixels (default: 600)"
    )

    parser.add_argument(
        "--fps", type=int, default=15, help="Frames per second (default: 15)"
    )

    parser.add_argument(
        "--start", type=int, default=None, help="Start frame (default: 0)"
    )

    parser.add_argument(
        "--end", type=int, default=None, help="End frame (default: last frame)"
    )

    parser.add_argument(
        "--no-gui", action="store_true", help="Disable GUI mode (sets OVITO_GUI_MODE=0)"
    )

    parser.add_argument(
        "--renderer",
        choices=["opengl"],
        default="opengl",
        help="Renderer backend (default: opengl)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # GUI mode toggle
    os.environ["OVITO_GUI_MODE"] = "0" if args.no_gui else "1"

    # Qt app (required by OVITO)
    app = PySide6.QtWidgets.QApplication([])

    print(f"Loading trajectory: {args.trajectory}")

    pipeline = import_file(args.trajectory)
    pipeline.add_to_scene()

    vp = Viewport()
    vp.zoom_all()

    # Determine frame range
    frame_start = args.start if args.start is not None else 0
    frame_end = args.end if args.end is not None else pipeline.source.num_frames

    # Renderer selection
    renderer = OpenGLRenderer() if args.renderer == "opengl" else OpenGLRenderer()

    print(f"Rendering from frame {frame_start} to frame {frame_end} to {args.output}")

    vp.render_anim(
        size=(args.width, args.height),
        filename=args.output,
        fps=args.fps,
        renderer=renderer,
        range=(frame_start, frame_end),
    )


if __name__ == "__main__":
    main()
