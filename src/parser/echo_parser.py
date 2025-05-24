import argparse
from parser import force_parser

echo_parser = argparse.ArgumentParser(
    description="Echo the given text to standard output", parents=[force_parser]
)
echo_parser.add_argument("content", help="Text to echo")
