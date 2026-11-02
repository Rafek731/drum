from drum.cli import parse_arguments
from drum.cli.interactive_prompt import InteractivePrompt
from drum.renderer import WolframRenderer

def main() -> int:
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
    main()
