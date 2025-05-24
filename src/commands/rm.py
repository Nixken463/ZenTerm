from argparse import Namespace
from pathlib import Path
import os

def execute_rm(self, args: Namespace) -> None:

        for target in args.targets:
            path = Path(target)
            if not path.exists():
                self.report_error(f"rm: cannot remove '{target}'; No such file or directory", args)
                continue

            if path.is_dir() and not args.recursive:
                if not args.d:
                    self.report_error(f"rm: cannot remove '{target}: Is a directory", args)
                    continue
                if args.d and len(os.listdir(path)) == 0:
                    if not self.interactive("rm: Remove", path.name,args):
                        continue
                    os.rmdir(path)
                    self.verbose(f"rm: Removed {path}", args)
                    continue
                else:
                    self.report_error(f"rm: directory not empty: {path}", args)
                    continue
            to_delete = []
            if path.is_dir():
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        to_delete.append(Path(root) / name)
                    for name in dirs:
                        to_delete.append(Path(root) / name)
                to_delete.append(path)  
            else:
                if not args.d:
                    to_delete.append(path)
                if args.d:
                    self.report_error(f"rm: Is a file: {path}", args)

            for item in to_delete:
                try:
                    if not self.interactive('rm: Remove', item, args ):
                        continue
                    if item.is_dir():
                        item.rmdir()
                    else:
                        item.unlink()

                    self.verbose(f"rm: Removed {item}", args)

                except PermissionError:
                    self.report_error(f"rm: Permission denied: {item}", args)

                except Exception as e:
                    self.report_error(f"rm: {e}", args)
