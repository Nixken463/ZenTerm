import argparse
from parser import force_parser, interactive_parser, verbose_parser

mv_parser = argparse.ArgumentParser(
    description="Move or rename files and directories",
    parents=[force_parser, interactive_parser, verbose_parser],
)
mv_parser.add_argument("source", help="Source file or directory to move")
mv_parser.add_argument("destination", help="Destination path or new name")
mv_parser.add_argument(
    "-r", "--recursive", action="store_true", help="Move directories with all contents"
)
