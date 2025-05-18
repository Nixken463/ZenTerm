from argparse import Namespace
from pathlib import Path
import os

def execute_rm(self, args: Namespace) -> None:

        for target in args.targets:
            path = Path(target)
            if not path.exists():
                self._report_error(f"rm: cannot remove '{target}'; No such file or directory", args)
                continue

            if path.is_dir() and not args.recursive:
                self._report_error(f"rm: cannot remove '{target}: Is a directory", args)
                return
            to_delete = []
            if path.is_dir():
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        to_delete.append(Path(root) / name)
                    for name in dirs:
                        to_delete.append(Path(root) / name)
                to_delete.append(path)  
            else:
                to_delete.append(path)

            for item in to_delete:
                try:
                    if not self._interactive('rm: Remove', item, args ):
                        continue
                    if item.is_dir():
                        item.rmdir()
                    else:
                        item.unlink()

                    self._verbose(f"rm: Removed {item}", args)

                except PermissionError:
                    self._report_error(f"rm: Permission denied: {item}", args)

                except Exception as e:
                    self._report_error(f"rm: {e}", args)
