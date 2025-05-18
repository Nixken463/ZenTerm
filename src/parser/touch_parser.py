import argparse
from parser import force_parser, interactive_parser, verbose_parser

touch_parser = argparse.ArgumentParser(description='Create one or more files', parents=[force_parser, interactive_parser, verbose_parser])
touch_parser.add_argument('path', nargs='+', help='One or more file paths to create or update')
