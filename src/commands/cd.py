from argparse import Namespace
from pathlib import Path
import os

def execute_cd(self, args: Namespace)-> None:
    path = args.path
    try:
        dir = Path(path).resolve(strict=True)
        os.chdir(dir)
    except FileNotFoundError:
        self.report_error(f"cd: No such directory: {path}",args)
    except NotADirectoryError:
        self.report_error(f"cd: Not a directory: {path}",args)
    except PermissionError:
        self.report_error(f"cd: Permission denied: {path}",args)
