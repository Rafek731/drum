"""Command-line argument parsing."""

import argparse
from pathlib import Path

from drum.config import RenderConfig


def parse_arguments() -> tuple[RenderConfig, Path]:
    """Parse the command-line options.

    On invalid arguments or --help, argparse prints a message and exits.

    Returns:
        The render settings and the directory to save GIFs to.

    Raises:
        ValueError: If the values are out of range (see RenderConfig).
    """
    parser = argparse.ArgumentParser(
        prog = "The Drum",
        description = "Generate gifs of vibrating drums",
        usage="drum [OPTIONS]"
    )
    parser.add_argument(
        "-A",
        "--amplitude",
        type=float,
        default=1.,
        help="Controls the amplitude of the wave. Defaults to 1."
    )
    parser.add_argument(
        "-m",
        "--mesh",
        type=int,
        default=15,
        help="Number of mesh lines on the plot. Defaults to 15."
    )
    parser.add_argument(
        "-t",
        "--total-frames",
        type=int,
        default=30,
        dest="total_frames",
        help="Number of frames in the animation (more = longer computation). Defaults to 30."
    )
    parser.add_argument(
        "-f",
        "--fps",
        "--frames-per-second",
        type=int,
        default=30,
        dest="fps",
        help="Controls how many frames should be in 1 second of the resulting gif. Defaults to 30."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd() / "Pictures",
        help="Specify the directory in which the gifs will be saved. Defaults to './Pictures'."
    )
    args = parser.parse_args()
    return (
        RenderConfig(
            args.amplitude,
            args.fps,
            args.total_frames,
            args.mesh,
        ),
        args.output
    )

