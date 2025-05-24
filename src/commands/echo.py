from argparse import Namespace

def execute_echo(self, args: Namespace) -> None:
        content = args.content
        try:
            self.poutput(content)
        except PermissionError:
            self.report_error(f"echo: Permission denied: {content}",args)
        except Exception as e:
            self.report_error(f"echo: Error: {e}",args)
