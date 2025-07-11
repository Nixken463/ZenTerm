from argparse import Namespace
from pathlib import Path

def execute_mkdir(self, args:Namespace) -> None:
    for dir in args.path: 
        if not self.interactive('mkdir: Create', dir, args):
            continue
        try: 
            if args.parents:
                Path(dir).mkdir(parents=True, exist_ok=True)
            else:
                Path(dir).mkdir(parents=False, exist_ok=False)
            self.verbose(f"mkdir: Created {dir}", args)
        except PermissionError:
            self.report_error(f"mkdir: Permission denied: {dir}", args)
        except FileExistsError:
            self.report_error(f"mkdir: Directory already exists: {dir}",args)
        except Exception as e:
            self.report_error(f"mkdir: Error creating directory: {e}", args)
