"""Plain data objects describing what to render and how."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RenderConfig:
    """Settings shared by every GIF rendered in one run.

    Attributes:
        amplitude: Maximum displacement of the membrane. The plot's z-range
            is fixed to [-1.1, 1.1], so values above 1.1 get clipped.
        fps: Frames per second of the resulting GIF.
        num_frames: Number of frames covering one full period of vibration.
        mesh: Number of mesh lines drawn on the surface in each direction.
    """

    amplitude: float
    fps: int
    num_frames: int
    mesh: int

    def __post_init__(self) -> None:
        """Validate the settings.

        Raises:
            ValueError: If fps or num_frames is below 1, or mesh is negative.
        """
        if self.fps < 1:
            raise ValueError("Frames per second cannot < 1.")
        if self.num_frames < 1:
            raise ValueError("GIF must have at least one frame.")
        if self.mesh < 0:
            raise ValueError("Number of mesh lines cannot be negative.")

@dataclass(frozen=True)
class Mode:
    """A normal mode (m, n) of a circular membrane.

    Attributes:
        m: Number of angular nodes
        n: Number of radial nodes
    """

    m: int
    n: int

    def __post_init__(self):
        """Validate the mode numbers.

        Raises:
            ValueError: If m is negative or n is below 1.
        """
        if self.m < 0:
            raise ValueError("m cannot be negative.")
        if self.n < 1:
            raise ValueError("n must be at least 1.")

# Wolfram script defining makeGif, loaded into the kernel by WolframRenderer
WL_SCRIPT_PATH = Path(__file__).parent / "wolfram" / "drum.wl"
