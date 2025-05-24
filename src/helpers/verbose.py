from argparse import Namespace


def verbose(self, message: str, args: Namespace):
    """Displays information about each action
    """
    if args.verbose:
        self.poutput(message)
