import argparse
from parser import force_parser

cd_parser = argparse.ArgumentParser(description='Change the current directory', parents=[force_parser])
cd_parser.add_argument('path', help='Target directory to switch into')