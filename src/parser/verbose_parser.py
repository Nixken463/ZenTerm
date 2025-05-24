import argparse

verbose_parser = argparse.ArgumentParser(add_help=False)
verbose_parser.add_argument(
    "-v", "--verbose", action="store_true", help="Display detailed progress information"
)
