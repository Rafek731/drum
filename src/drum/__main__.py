"""Entry point of the drum command."""

from drum.cli import parse_arguments
from drum.cli.interactive_prompt import InteractivePrompt
from drum.renderer import WolframRenderer


def main() -> int:
    """Run the interactive drum CLI.

    Parses the options, starts one Wolfram session and renders a GIF for
    every mode the user enters until they quit. Render errors are printed
    and the prompt continues.

    Returns:
        The exit code (0 on normal quit).
    """
    render_config, outdir = parse_arguments()
    prompt = InteractivePrompt()
    prompt.welcome()

    with WolframRenderer(render_config, outdir) as renderer:
        for mode in prompt.modes():
            try:
                path = renderer.render(mode)
            except RuntimeError as e:
                print(e)
                continue
            print(f"Saved {path}\n")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
