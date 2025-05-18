from argparse import Namespace
def report_error(self,message: str, args: Namespace):
        """
        Write out error messages
        """
        if not args.force:
            self.perror(message)
    