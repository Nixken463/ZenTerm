import argparse
from parser import force_parser, interactive_parser, verbose_parser

cp_parser = argparse.ArgumentParser(description='Copy files from source to destination', parents=[force_parser, interactive_parser, verbose_parser])
cp_parser.add_argument('source', help='Existing file to copy')
cp_parser.add_argument('destination', help='Target path for the copied file')
cp_parser.add_argument('-r', '--recursive', action='store_true', help="Copy folder with all contents")
