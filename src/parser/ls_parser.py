import argparse
from parser import force_parser

ls_parser = argparse.ArgumentParser(description='List directory contents', parents=[force_parser])
ls_parser.add_argument('path', nargs='?', default='.', help='Directory to list (default: current directory)')
ls_parser.add_argument('-a', '--all', action="store_true", help="Include hidden files")

