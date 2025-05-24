import argparse
from parser import force_parser

ls_parser = argparse.ArgumentParser(description='List directory contents', parents=[force_parser])
ls_parser.add_argument('path', nargs='?', default='.', help='Directory to list (default: current directory)')
ls_parser.add_argument('-a', '--all', action="store_true", help="Include hidden files")
ls_parser.add_argument('-l', '--long', action="store_true", help="List files in long format")
ls_parser.add_argument('-r', '--reverse', action="store_true", help="List in reverse order")
ls_parser.add_argument('-S', action="store_true",dest='S', help="Sort by file size")
ls_parser.add_argument('-s', action="store_true", help="List file size")

