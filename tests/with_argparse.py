#Made by Nixken
import os, sys
from cmd2 import Cmd, with_argparser
from pathlib import Path
import argparse
import shutil
# base, often reused flags
base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument('-f', '--force', action='store_true', help='Suppress errors and force the operation')
base_parser.add_argument('-i', '--interactive', action='store_true', help='Prompt for confirmation before each action')
base_parser.add_argument('-v', '--verbose', action='store_true', help='Provide detailed output during execution')

rm_parser = argparse.ArgumentParser(parents=[base_parser])
rm_parser.add_argument('-r', '--recursive', action='store_true', help='Recursively delete directories')
rm_parser.add_argument('targets', nargs='+', help='Files or directories to remove')

class ZenShell(Cmd):
    def __init__(self):
        super().__init__()
        self.stdout = sys.stdout
    @property
    def prompt(self):
        return f"-> {Path.cwd().name} "


    def do_cd(self, path):
            try:
                dir = Path(path).resolve(strict=True)
                os.chdir(dir)
            except FileNotFoundError:
                self.perror(f"cd: No such directory: {path}")
            except NotADirectoryError:
                self.perror(f"cd: Not a directory: {path}")
            except PermissionError:
                self.perror(f"cd: Permission denied: {path}")
            except:
                self.perror(f"cd: No such file or directory: {path}")

    def do_exit(self, _):
        return True



    def do_mkdir(self, arg):
        parser = argparse.ArgumentParser(parents=[base_parser])
        parser.add_argument('-p', '--parents', action="store_true", help="create parent directory if not existing")
        parser.add_argument('path', default=".", help="Location and name of the directory to create")

        try:
            parse = parser.parse_args(arg.split())
        except SystemExit:
            return


        path = Path(parse.path)
        
        try: 
            if parse.parents:
                path.mkdir(parents=True, exist_ok=False)
            else:
                path.mkdir(parents=False, exist_ok=False)

        except PermissionError:
            self.perror(f"mkdir: Permission denied: {path}")
        except FileExistsError:
            self.perror(f"mkdir: Directory already exists: {path}")
        except Exception as e:
            self.perror(f"mkdir: Error creating directory: {e}")


    @with_argparser(rm_parser)        
    def do_rm(self, args):

        def confirm(path):
            resp = input(f"rm: remove {'directory' if path.is_dir() else 'file'} '{path}'? (y/n) ").strip().lower()
            return resp == 'y'

        for target in args.targets:
            path = Path(target)
            if not path.exists():
                if not args.force:
                    self.perror(f"rm: cannot remove '{target}': No such file or directory")
                continue

            if path.is_dir() and not args.recursive:
                if not args.force:
                    self.perror(f"rm: cannot remove '{target}': Is a directory")
                continue

            to_delete = []
            if path.is_dir():
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        to_delete.append(Path(root) / name)
                    for name in dirs:
                        to_delete.append(Path(root) / name)
                to_delete.append(path)  
            else:
                to_delete.append(path)

            for item in to_delete:
                try:
                    if args.interactive and not confirm(item):
                        continue

                    if item.is_dir():
                        item.rmdir()
                    else:
                        item.unlink()

                    if args.verbose:
                        self.poutput(f"Removed: {item}")
                except PermissionError:
                    self.perror(f"rm: Permission denied: {item}")


                except Exception as e:
                    if not args.force:
                        self.perror(f"rm: cannot remove '{item}': {e}")

    def do_touch(self, path):
    
        path = Path(path)
        try:
            path.touch(exist_ok=True)
        except PermissionError:
            self.perror(f"touch: Permission denied: {path}")
        except Exception as e:
            self.perror(f"Error: {e}")
    

    


    def do_ls(self,arg):
        parser = argparse.ArgumentParser(parents=[base_parser])
        parser.add_argument('path', nargs="?", default=".", help="Path to the ls location")
        try:
            parse = parser.parse_args(arg.split())
        except SystemExit:
            return
        try:
            entries =  []
            path = Path(parse.path)
            for entry in sorted(path.iterdir()):

                name = f"{entry.name}/" if entry.is_dir() else entry.name
                entries.append(name)

            self.poutput(" ".join(entries))

        except FileNotFoundError:
            self.perror(f"ls: No such directory: {parse.path}")

        except Exception as e:
            self.perror(f"Error: {e}")

if __name__ == "__main__":
    ZenShell().cmdloop()
