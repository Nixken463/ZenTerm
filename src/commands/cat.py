from pathlib import Path
from argparse import Namespace

def execute_cat(self, args: Namespace) -> None:
        path = Path(args.path)

        try:
            if Path(path).is_dir():
                self._report_error(f"cat: {path.name} is a directory",args)
                return
            else:
                content = path.read_text(encoding="utf-8", errors="strict")
                self.poutput(content)
        except FileNotFoundError:
            self._report_error(f"cat: No such file: {path}",args)

        except PermissionError:
            self._report_error(f"cat: Permission denied: {path}",args)

        except UnicodeDecodeError:
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                self.poutput(content)            
                self._report_error(f"cat: Warning — invalid UTF‑8 sequences in {path}, showing � for invalid bytes",args)
            except UnicodeDecodeError:
                try:
                    content = path.read_text(encoding="iso-8859-1", errors="replace")
                    self.poutput(content)
                    self._report_error(f"cat: Decoded {path} with iso-8859-1 (fallback)",args)
                except  Exception:
                    self._report_error(f"cat: Unable to decode {path}",args)
