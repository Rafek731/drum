"""Interactive prompt that reads mode numbers from the user."""

import re
from collections.abc import Iterator

from drum.config import Mode


class InteractivePrompt:
    """Asks the user for mode numbers until they quit.

    Attributes:
        WELCOME: Message printed once at startup.
        PROMPT: Text shown before each input.
        MODE_REGEXP: Accepted input format: two non-negative integers
            separated by whitespace, e.g. '1 3'.
        QUIT_COMMANDS: Inputs (case-insensitive) that end the prompt.
    """

    WELCOME: str = "Welcome to drum!\nSetting up the kernels..."
    PROMPT: str = "Provide mode numbers 'm n' or 'q' to quit\n-> "
    MODE_REGEXP: re.Pattern = re.compile(r"(\d+)\s+(\d+)")
    QUIT_COMMANDS: frozenset[str] = frozenset({"q", "quit"})

    def modes(self) -> Iterator[Mode]:
        """Yield valid modes typed by the user until they quit.

        Invalid input prints an error and asks again. The prompt ends on
        'q', 'quit', Ctrl+D or Ctrl+C.

        Yields:
            Each valid mode the user enters.
        """
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
        """Convert input like '1 3' into a Mode.

        Args:
            user_input: Text typed by the user, already stripped.

        Returns:
            The parsed mode.

        Raises:
            ValueError: If the input isn't two integers, or the numbers
                aren't a valid mode (see Mode).
        """
        match = self.MODE_REGEXP.fullmatch(user_input)

        if match is None:
            raise ValueError(
                f"Invalid mode numbers passed: {user_input!r}. Expected two integers, e.g. '1 3'."
            )

        m, n = map(int, match.groups())
        return Mode(m, n)

    def welcome(self) -> None:
        """Print the welcome message."""
        print(self.WELCOME)
