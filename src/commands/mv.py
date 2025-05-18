from argparse import Namespace
from pathlib import Path
import shutil

def execute_mv(self, args: Namespace) -> None:
    
        source_path = Path(args.source)
        destination_path = Path(args.destination)

        try:
            if source_path.exists():
                if not  self._interactive(f"mv: Move", source_path,args):
                    return
                if destination_path.parent.exists() and destination_path.parent.is_dir():
                    if source_path.is_dir() and not args.recursive:
                        self._report_error(f"mv: Is a directory: {source_path}", args)
                        return
                    shutil.move(source_path, destination_path)
                    self._verbose(f"mv: Moved {source_path} to {destination_path}", args)
                else:
                    self._report_error(f"mv: No such directory: {destination_path}",args)
            else:
                self._report_error(f"mv: No such file or directory: {source_path}",args)
        except PermissionError:
            self._report_error(f"mv: Permission denied: {destination_path}", args)
        except FileNotFoundError:
            self._report_error(f"mv: No such file or directory: {source_path}", args)
