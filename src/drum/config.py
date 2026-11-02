from dataclasses import dataclass
from pathlib import Path

@dataclass
class RenderConfig:
    amplitude: float
    fps: int
    num_frames: int
    mesh: int

    def __post_init__(self) -> None:
        if self.fps < 1:
            raise ValueError("Frames per second cannot < 1.")
        if self.num_frames < 1:
            raise ValueError("GIF must have at least one frame.")
        if self.mesh < 0:
            raise ValueError("Number of mesh lines cannot be negative.")

@dataclass
class Mode:
    m: int
    n: int

    def __post_init__(self):
        if self.m < 0:
            raise ValueError("m cannot be negative.")
        if self.n < 1:
            raise ValueError("n must be at least 1.")
