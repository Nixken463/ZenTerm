import argparse

force_parser = argparse.ArgumentParser(add_help=False)
force_parser.add_argument('-f', '--force', action='store_true', help='Ignore errors and proceed without prompting')
