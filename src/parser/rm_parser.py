import argparse
from parser import force_parser, interactive_parser, verbose_parser

rm_parser = argparse.ArgumentParser(description='Remove files or directories', parents=[force_parser, interactive_parser, verbose_parser])
rm_parser.add_argument('-r', '--recursive', action='store_true', help='Recursively delete directories and their contents')
rm_parser.add_argument('targets', nargs='+', help='One or more file or directory paths to remove')