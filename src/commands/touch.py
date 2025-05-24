from pathlib import Path
from argparse import Namespace


def execute_touch(self, args: Namespace) -> None:
    for file in args.path:
        if not self.interactive("touch: Create", file, args):
            continue
        try:
            Path(file).touch(exist_ok=True)
            self.verbose(f"touch: Created {file}", args)

        except PermissionError:
            self.report_error(f"touch: Permission denied: {file}", args)
        except Exception as e:
            self.report_error(f"touch: {e}", args)
