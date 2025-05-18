import argparse
from parser import force_parser

cat_parser = argparse.ArgumentParser(description='Concatenate and display file content', parents=[force_parser])
cat_parser.add_argument('path', help='Path of the file to display')
