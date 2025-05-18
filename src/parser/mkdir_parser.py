import argparse
from parser import force_parser, interactive_parser, verbose_parser

mkdir_parser = argparse.ArgumentParser(description='Create one or more directories', parents=[force_parser, interactive_parser, verbose_parser])
mkdir_parser.add_argument('-p', '--parents', action='store_true', help='Make parent directories as needed (like mkdir -p)')
mkdir_parser.add_argument('path', nargs='+', help='One or more directory paths to create')
