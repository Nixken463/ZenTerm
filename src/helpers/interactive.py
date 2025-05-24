from argparse import Namespace
from pathlib import Path


# The first parameter 'shell_instance' will be the ZenShell object
def interactive(self, action: str, item: Path, args: Namespace) -> bool:
    """Ask for confirmation before each action.
    """
    if not (hasattr(args, "interactive") and args.interactive):
        return True

    try:
        prompt_message = f"{action} '{item}'? (y/N) "
        response = self.read_input(prompt_message).strip().lower()
        return response == "y"
    except (EOFError, KeyboardInterrupt):
        self.poutput("")

        return False
