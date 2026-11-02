"""Rendering of membrane GIFs through a Wolfram kernel."""

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl

from drum.config import WL_SCRIPT_PATH, Mode, RenderConfig


@dataclass
class WolframRenderer:
    """Renders modes to GIFs using one Wolfram session.

    Use as a context manager: entering starts the kernel and loads drum.wl
    (which launches the parallel subkernels), exiting stops it. Starting the
    kernels takes a few seconds, so reuse one renderer for many modes.

    Attributes:
        config: Settings applied to every rendered GIF.
        outdir: Directory the GIFs are saved to.
    """

    config: RenderConfig
    outdir: Path
    _session: WolframLanguageSession = field(init=False)

    def __post_init__(self):
        """Create the session (not started yet) and the output directory."""
        self._session = WolframLanguageSession(kernel=shutil.which("WolframKernel"))
        self.outdir.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        """Start the kernel, load drum.wl and return the renderer."""
        self._session.start()
        self._session.evaluate(wl.Get(str(WL_SCRIPT_PATH)))
        return self

    def __exit__(self, exc_type, exc, tb):
        """Stop the kernel together with its subkernels."""
        self._session.stop()

    def render(self, mode: Mode) -> Path:
        """Render one mode to a GIF named mode_<m>_<n>.gif.

        Args:
            mode: The mode to render.

        Returns:
            Path of the saved GIF.

        Raises:
            RuntimeError: If the kernel reported an error or Export failed.
        """
        print("Munching...")
        c = self.config
        path = self.outdir / f"mode_{mode.m}_{mode.n}.gif"

        result = self._session.evaluate_wrap(
            wl.Global.makeGif(
                mode.m, mode.n, str(path),
                wl.Rule("Amplitude", c.amplitude),
                wl.Rule("Mesh", c.mesh),
                wl.Rule("Frames", c.num_frames),
                wl.Rule("FPS", c.fps),
            )
        )

        if not result.success or result.result != str(path):
            raise RuntimeError(f"Wolfram failed to render {path}: {result.messages}")
        print("Done!")
        return path
