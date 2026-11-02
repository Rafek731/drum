import re
from collections.abc import Iterator
from drum.config import Mode

class InteractivePrompt:
    WELCOME: str = "Welcome to drum!\nSetting up the kernels..."
    PROMPT: str = "Provide mode numbers 'm n' or 'q' to quit\n-> "
    MODE_REGEXP: re.Pattern = re.compile(r"(\d+)\s+(\d+)")
    QUIT_COMMANDS: frozenset[str] = frozenset({"q", "quit"})

    def modes(self) -> Iterator[Mode]:
        """Yield valid modes typed by the user until they quit."""
        while True:
            try:
                user_input = input(self.PROMPT).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return

            if user_input.lower() in self.QUIT_COMMANDS:
                return

            try:
                mode = self.parse_mode(user_input)
            except ValueError as e:
                print(e)
                continue

            yield mode

    def parse_mode(self, user_input: str) -> Mode:
        match = self.MODE_REGEXP.fullmatch(user_input)

        if match is None:
            raise ValueError(
                f"Invalid mode numbers passed: {user_input!r}. Expected two integers, e.g. '1 3'."
            )

        m, n = map(int, match.groups())
        return Mode(m, n)

    def welcome(self) -> None:
        print(self.WELCOME)
