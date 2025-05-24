from argparse import Namespace


def execute_clear(self, args: Namespace) -> None:
    self.poutput("\033c")
