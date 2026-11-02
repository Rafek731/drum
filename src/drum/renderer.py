import shutil
from dataclasses import dataclass, field
from drum.config import Mode, RenderConfig, WL_SCRIPT_PATH
from pathlib import Path
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl


@dataclass
class WolframRenderer:
    config: RenderConfig
    outdir: Path
    _session: WolframLanguageSession = field(init=False)

    def __post_init__(self):
        # wolframclient doesn't search /usr/local/Wolfram/Wolfram/<version>,
        # so use the kernel on PATH; None falls back to its own search
        self._session = WolframLanguageSession(kernel=shutil.which("WolframKernel"))
        self.outdir.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        self._session.start()
        self._session.evaluate(wl.Get(str(WL_SCRIPT_PATH)))
        return self

    def __exit__(self, exc_type, exc, tb):
        self._session.stop()

    def render(self, mode: Mode) -> Path:
        print("Munching...")
        c = self.config
        path = self.outdir / f"membrane_{mode.m}_{mode.n}.gif"

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
