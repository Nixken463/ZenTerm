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

mkdir_parser = argparse.ArgumentParser(parents=[base_parser])
mkdir_parser.add_argument('-p', '--parents', action="store_true", help="create parent directory if not existing")
mkdir_parser.add_argument('path', default=".", nargs="+", help="Location and name of the directory to create")

ls_parser = argparse.ArgumentParser(parents=[base_parser])
ls_parser.add_argument('path', nargs="?", default=".", help="Path to the ls location")

mv_parser = argparse.ArgumentParser(parents=[base_parser])
mv_parser.add_argument('source', help="Path to the source file")
mv_parser.add_argument('destination', help="Path to the destination")

cp_parser = argparse.ArgumentParser(parents=[base_parser])
cp_parser.add_argument('source', help="Path to the source file")
cp_parser.add_argument('destination', help="Path to the destination")

touch_parser = argparse.ArgumentParser(parents=[base_parser])
touch_parser.add_argument('path',nargs="+",default=".", help="Path for the created file")





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

    @with_argparser(mv_parser)
    def do_mv(self, args):
        source_path = Path(args.source)
        destination_path = Path(args.destination)

        try:
            if source_path.exists():
                if destination_path.parent.exists() and destination_path.parent.is_dir():
                    shutil.move(source_path, destination_path)
                else:
                    self.perror(f"mv: No such directory: {destination_path}")
            else:
                self.perror(f"mv: No such file or directory: {source_path}")
        except PermissionError:
            self.perror(f"mv: Permission denied: {destination_path}")
        except FileNotFoundError:
            self.perror(f"mv: No such file or directory: {source_path}")

    @with_argparser(cp_parser)
    def do_cp(self, args):
        source_path = Path(args.source)
        destination_path = Path(args.destination)
        try:
            if source_path.exists():
                if destination_path.parent.exists() and destination_path.parent.is_dir():
                    shutil.copy2(source_path, destination_path)
                else:
                    self.perror(f"cp: No such directory: {destination_path.parent}")
            
        except PermissionError:
            self.perror(f"cp: Permissiond denied: {destination_path.parent}")
        except FileNotFoundError:
            self.perror(f"cp: No such file or directory: {source_path}")
        except Exception as e:
            self.perror(f"cp: Error: {e}")



    def do_clear(self, _):
        self.poutput("\033c")

    def do_cat(self, path):
        path = Path(path.strip())

        try:
            if Path(path).is_dir():
                self.perror(f"cat: {path.name} is a directory")
                return
            else:
                content = path.read_text(encoding="utf-8", errors="strict")
                self.poutput(content)
        except FileNotFoundError:
            self.perror(f"cat: No such file: {path}")

        except PermissionError:
            self.perror(f"cat: Permission denied: {path}")

        except UnicodeDecodeError:
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                self.poutput(content)            
                self.perror(f"cat: Warning — invalid UTF‑8 sequences in {path}, showing � for invalid bytes")
            except UnicodeDecodeError:
                try:
                    content = path.read_text(encoding="iso-8859-1", errors="replace")
                    self.poutput(content)
                    self.perror(f"cat: Decoded {path} with iso-8859-1 (fallback)")
                except  Exception:
                    self.perror(f"cat: Unable to decode {path}")



    def do_echo(self, call):
        try:
            self.poutput(call)
        except PermissionError:
            self.perror(f"echo: Permission denied: {call}")
        except Exception as e:
            self.perror(f"echo: Error: {e}")

    @with_argparser(mkdir_parser)
    def do_mkdir(self, args):
        
        for dir in args.path: 
            try: 
                if args.parents:
                    Path(dir).mkdir(parents=True, exist_ok=False)
                else:
                    Path(dir).mkdir(parents=False, exist_ok=False)

            except PermissionError:
                self.perror(f"mkdir: Permission denied: {dir}")
            except FileExistsError:
                self.perror(f"mkdir: Directory already exists: {dir}")
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

    @with_argparser(touch_parser)
    def do_touch(self, args):

        for file in args.path:
            try:
                Path(file).touch(exist_ok=False)
            except PermissionError:
                self.report_error(f"touch: Permission denied: {file}", args)
            except FileExistsError:
                self.report_error(f"touch: File already exists: {file}",args)
            except Exception as e:
                self.report_error(f"touch: {e}", args) 
    def report_error(self,message: str, args):
        if not args.force:
            self.perror(message)

    def do_pwd(self, _):
        self.poutput(Path.cwd())
    

    @with_argparser(ls_parser)
    def do_ls(self,args):
        
        try:
            entries =  []
            path = Path(args.path)
            for entry in sorted(path.iterdir()):

                name = f"{entry.name}/" if entry.is_dir() else entry.name
                entries.append(name)

            self.poutput(" ".join(entries))

        except FileNotFoundError:
            self.perror(f"ls: No such directory: {args.path}")

        except Exception as e:
            self.perror(f"Error: {e}")

if __name__ == "__main__":
    os.chdir("/home/nix/Code/Python/ZenTerm/tests")
    ZenShell().cmdloop()
