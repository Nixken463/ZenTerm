from argparse import Namespace
from pathlib import Path

def execute_pwd(self, args: Namespace) -> None:
    self.poutput(Path.cwd())