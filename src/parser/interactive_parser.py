import argparse

interactive_parser = argparse.ArgumentParser(add_help=False)
interactive_parser.add_argument('-i', '--interactive', action='store_true', help='Ask for confirmation before each action')
