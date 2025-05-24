from argparse import Namespace
from pathlib import Path
import shutil


def execute_cp(self, args: Namespace) -> None:
    source_path = Path(args.source)
    destination_path = Path(args.destination)
    try:
        if not source_path.exists():
            self.report_error(f"cp: No such file or directory: {source_path}", args)
            return
        if not self.interactive("cp: Copy", source_path, args):
            return
        actual_target: Path
        if destination_path.is_dir():
            actual_target = destination_path / source_path.name
        else:
            actual_target = destination_path

        if source_path.is_dir() and not args.recursive:
            self.report_error(f"cp: Is a directory: {source_path}", args)
            return
        elif source_path.is_dir() and args.recursive:
            shutil.copytree(source_path, actual_target, dirs_exist_ok=True)
            self.verbose(
                f"Copied all files of {source_path} to {destination_path}", args
            )
            return
        elif source_path.is_file():
            shutil.copy2(source_path, destination_path)
            self.verbose(f"cp: Copied {source_path} to {destination_path.parent}", args)
    except PermissionError:
        self.report_error(f"cp: Permission denied: {destination_path.parent}", args)
    except FileNotFoundError:
        self.report_error(f"cp: No such file or directory: {destination_path}", args)
    except NotADirectoryError:
        self.report_error(f"cp: Is not a directory: {destination_path.parent}", args)
