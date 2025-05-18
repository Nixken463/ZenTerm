from argparse import Namespace
from pathlib import Path

def execute_ls(self,args: Namespace) -> None:
        try:
            entries =  []
            path = Path(args.path)

            for entry in sorted(p for p in path.iterdir() if args.all or not p.name.startswith('.')):

                name = f"{entry.name}/" if entry.is_dir() else entry.name
                entries.append(name)

            self.poutput(" ".join(entries))

        except FileNotFoundError:
            self._report_error(f"ls: No such file or Directory {args.path}", args)
        except Exception as e:
            self._report_error(f"ls: {e}", args)
