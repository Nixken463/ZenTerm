#Made by Nixken
import os, sys
from cmd2 import Cmd, with_argparser
from pathlib import Path
import argparse
# base, often reused flags
base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument('-f', '--force', action='store_true', help='Suppress errors and force the operation')
base_parser.add_argument('-i', '--interactive', action='store_true', help='Prompt for confirmation before each action')
base_parser.add_argument('-v', '--verbose', action='store_true', help='Provide detailed output during execution')
class ZenShell(Cmd):
    def __init__(self):
        super().__init__()
        self.stdout = sys.stdout
        self.poutput("""
        ███████╗███████╗███╗░░██╗████████╗███████╗██████╗░███╗░░░███╗
        ╚════██║██╔════╝████╗░██║╚══██╔══╝██╔════╝██╔══██╗████╗░████║
        ░░███╔═╝█████╗░░██╔██╗██║░░░██║░░░█████╗░░██████╔╝██╔████╔██║
        ██╔══╝░░██╔══╝░░██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██║╚██╔╝██║
        ███████╗███████╗██║░╚███║░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
        ╚══════╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝
        """) 
    @property
    def prompt(self):
        return f"{Path.cwd().name} "


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

    def do_cat(self, filename):
        path = Path(filename.strip())
        try:
            content = path.read_text(encoding="utf-8")
            self.poutput(content)
        except FileNotFoundError:
            self.perror(f"cat: No such file: {filename}")





    def do_rm(self, arg):
        parser = argparse.ArgumentParser(parents=[base_parser], add_help=False)
        parser.add_argument('-r', '--recursive', action='store_true', help='Recursively delete directories')
        parser.add_argument('targets', nargs='+', help='Files or directories to remove')
        try:
            parse = parser.parse_args(arg.split())
        except SystemExit:
            return

        def confirm(path):
            resp = input(f"rm: remove {'directory' if path.is_dir() else 'file'} '{path}'? (y/n) ").strip().lower()
            return resp == 'y'

        for target in parse.targets:
            path = Path(target)
            if not path.exists():
                if not parse.force:
                    self.perror(f"rm: cannot remove '{target}': No such file or directory")
                continue

            if path.is_dir() and not parse.recursive:
                if not parse.force:
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
                    if parse.interactive and not confirm(item):
                        continue

                    if item.is_dir():
                        item.rmdir()
                    else:
                        item.unlink()

                    if parse.verbose:
                        self.poutput(f"Removed: {item}")
                except Exception as e:
                    if not parse.force:
                        self.perror(f"rm: cannot remove '{item}': {e}")

    def do_touch(self, path):
    
        path = Path(path)
        try:
            path.touch(exist_ok=True)
        except PermissionError:
            self.perror("You dont have Permission to create a file")
        except Exception as e:
            self.perror(f"Error: {e}")
    

    def do_pwd(self, _):
        self.poutput(Path.cwd())
    


    def do_ls(self, directory):
        try:
            entries =  []
            path = Path.cwd()
            path = Path(directory).expanduser().resolve()
            for entry in sorted(path.iterdir()):

                name = f"{entry.name}/" if entry.is_dir() else entry.name
                entries.append(name)

            self.poutput(" ".join(entries))

        except FileNotFoundError:
            self.perror(f"ls: No such directory: {directory}")

        except Exception as e:
            self.perror(f"Error: {e}")

if __name__ == "__main__":
    ZenShell().cmdloop()
