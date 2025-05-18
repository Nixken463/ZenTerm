#Made by Nixken
import os, sys
from cmd2 import Cmd, with_argparser
from pathlib import Path
from argparse import Namespace
import argparse
import shutil

force_parser = argparse.ArgumentParser(add_help=False)
force_parser.add_argument('-f', '--force', action='store_true', help='Ignore errors and proceed without prompting')

interactive_parser = argparse.ArgumentParser(add_help=False)
interactive_parser.add_argument('-i', '--interactive', action='store_true', help='Ask for confirmation before each action')

verbose_parser = argparse.ArgumentParser(add_help=False)
verbose_parser.add_argument('-v', '--verbose', action='store_true', help='Display detailed progress information')

rm_parser = argparse.ArgumentParser(description='Remove files or directories', parents=[force_parser, interactive_parser, verbose_parser])
rm_parser.add_argument('-r', '--recursive', action='store_true', help='Recursively delete directories and their contents')
rm_parser.add_argument('targets', nargs='+', help='One or more file or directory paths to remove')

mkdir_parser = argparse.ArgumentParser(description='Create one or more directories', parents=[force_parser, interactive_parser, verbose_parser])
mkdir_parser.add_argument('-p', '--parents', action='store_true', help='Make parent directories as needed (like mkdir -p)')
mkdir_parser.add_argument('path', nargs='+', help='One or more directory paths to create')

ls_parser = argparse.ArgumentParser(description='List directory contents', parents=[force_parser])
ls_parser.add_argument('path', nargs='?', default='.', help='Directory to list (default: current directory)')
ls_parser.add_argument('-a', '--all', action="store_true", help="Include hidden files")

mv_parser = argparse.ArgumentParser(description='Move or rename files and directories', parents=[force_parser, interactive_parser, verbose_parser])
mv_parser.add_argument('source', help='Source file or directory to move')
mv_parser.add_argument('destination', help='Destination path or new name')
mv_parser.add_argument('-r', '--recursive', action='store_true', help="Move directories with all contents")

cp_parser = argparse.ArgumentParser(description='Copy files from source to destination', parents=[force_parser, interactive_parser, verbose_parser])
cp_parser.add_argument('source', help='Existing file to copy')
cp_parser.add_argument('destination', help='Target path for the copied file')
cp_parser.add_argument('-r', '--recursive', action='store_true', help="Copy folder with all contents")
touch_parser = argparse.ArgumentParser(description='Create one or more files', parents=[force_parser, interactive_parser, verbose_parser])
touch_parser.add_argument('path', nargs='+', help='One or more file paths to create or update')

cat_parser = argparse.ArgumentParser(description='Concatenate and display file content', parents=[force_parser])
cat_parser.add_argument('path', help='Path of the file to display')

echo_parser = argparse.ArgumentParser(description='Echo the given text to standard output', parents=[force_parser])
echo_parser.add_argument('content', help='Text to echo')

cd_parser = argparse.ArgumentParser(description='Change the current directory', parents=[force_parser])
cd_parser.add_argument('path', help='Target directory to switch into')

exit_parser = argparse.ArgumentParser(description='Exit the shell')

clear_parser = argparse.ArgumentParser(description='Clear contents of the Shell')

pwd_parser = argparse.ArgumentParser(description='Show current working directory')


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

    @with_argparser(cd_parser)
    def do_cd(self, args: Namespace)-> None:
        """
        Change the working directory. Supports: -h
        """
        path = args.path
        try:
            dir = Path(path).resolve(strict=True)
            os.chdir(dir)
        except FileNotFoundError:
            self._report_error(f"cd: No such directory: {path}",args)
        except NotADirectoryError:
            self._report_error(f"cd: Not a directory: {path}",args)
        except PermissionError:
            self._report_error(f"cd: Permission denied: {path}",args)
        except:
            self._report_error(f"cd: No such file or directory: {path}",args)

    @with_argparser(exit_parser)
    def do_exit(self, args:Namespace)-> bool:
        """
        Quit the shell. Supports: -h
        """
        return True

    @with_argparser(mv_parser)
    def do_mv(self, args: Namespace) -> None:
        """
        Move files or directories. Supports: -f -r -v -i
        """
        source_path = Path(args.source)
        destination_path = Path(args.destination)

        try:
            if source_path.exists():
                if not  self._interactive(f"mv: Move", source_path,args):
                    return
                if destination_path.parent.exists() and destination_path.parent.is_dir():
                    if source_path.is_dir() and not args.recursive:
                        self._report_error(f"mv: Is a directory: {source_path}", args)
                        return
                    shutil.move(source_path, destination_path)
                    self._verbose(f"mv: Moved {source_path} to {destination_path}", args)
                else:
                    self._report_error(f"mv: No such directory: {destination_path}",args)
            else:
                self._report_error(f"mv: No such file or directory: {source_path}",args)
        except PermissionError:
            self._report_error(f"mv: Permission denied: {destination_path}", args)
        except FileNotFoundError:
            self._report_error(f"mv: No such file or directory: {source_path}", args)

    @with_argparser(cp_parser)
    def do_cp(self, args: Namespace) -> None:
        """
        Copy files or directories. Supports: -f -r -v -i
        """
        source_path = Path(args.source)
        destination_path = Path(args.destination)
        try:
            if not source_path.exists():
                self._report_error(f"cp: No such file or directory: {source_path}", args)
                return
            if not self._interactive('cp: Copy',source_path, args):
                return
            actual_target: Path 
            if destination_path.is_dir():
                actual_target = destination_path / source_path.name
            else:
                actual_target = destination_path

            if source_path.is_dir() and not args.recursive:
                self._report_error(f"cp: Is a directory: {source_path}",args)
                return
            elif source_path.is_dir() and args.recursive:
        
                shutil.copytree(source_path, actual_target, dirs_exist_ok=True)
                self._verbose(f"Copied all files of {source_path} to {destination_path}", args)
                return
            elif source_path.is_file():
                shutil.copy2(source_path, destination_path)
                self._verbose(f"cp: Copied {source_path} to {destination_path.parent}", args)
                 
        except PermissionError:
            self._report_error(f"cp: Permission denied: {destination_path.parent}",args)
        except FileNotFoundError:
            self._report_error(f"cp: No such file or directory: {destination_path}",args)
        except NotADirectoryError:
            self._report_error(f"cp: Is not a directory: {destination_path.parent}", args)
    


    @with_argparser(clear_parser)
    def do_clear(self, args: Namespace) -> None:
        """
        Clear the contents of the shell. Supports: -h
        """
        self.poutput("\033c")

    @with_argparser(cat_parser)
    def do_cat(self, args: Namespace) -> None:

        """
        Concatenate and display file content. Supports: -f -h
        """
        path = Path(args.path)

        try:
            if Path(path).is_dir():
                self._report_error(f"cat: {path.name} is a directory",args)
                return
            else:
                content = path.read_text(encoding="utf-8", errors="strict")
                self.poutput(content)
        except FileNotFoundError:
            self._report_error(f"cat: No such file: {path}",args)

        except PermissionError:
            self._report_error(f"cat: Permission denied: {path}",args)

        except UnicodeDecodeError:
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                self.poutput(content)            
                self._report_error(f"cat: Warning — invalid UTF‑8 sequences in {path}, showing � for invalid bytes",args)
            except UnicodeDecodeError:
                try:
                    content = path.read_text(encoding="iso-8859-1", errors="replace")
                    self.poutput(content)
                    self._report_error(f"cat: Decoded {path} with iso-8859-1 (fallback)",args)
                except  Exception:
                    self._report_error(f"cat: Unable to decode {path}",args)



    @with_argparser(echo_parser)
    def do_echo(self, args: Namespace) -> None:
        """
        Echo the given text to standard output
        """
        content = args.content
        try:
            self.poutput(content)
        except PermissionError:
            self._report_error(f"echo: Permission denied: {content}",args)
        except Exception as e:
            self._report_error(f"echo: Error: {e}",args)

    @with_argparser(mkdir_parser)
    def do_mkdir(self, args:Namespace) -> None:
        """
        Create one or more directories. Supports: -p -i -v -f.
        """ 
        
        for dir in args.path: 
            if not self._interactive('mkdir: Create', dir, args):
                continue
            try: 
                if args.parents:
                    Path(dir).mkdir(parents=True, exist_ok=True)
                else:
                    Path(dir).mkdir(parents=False, exist_ok=False)
                self._verbose(f"mkdir: Created {dir}", args)
            except PermissionError:
                self._report_error(f"mkdir: Permission denied: {dir}", args)
            except FileExistsError:
                self._report_error(f"mkdir: Directory already exists: {dir}",args)
            except Exception as e:
                self._report_error(f"mkdir: Error creating directory: {e}", args)


    @with_argparser(rm_parser) 
    def do_rm(self, args: Namespace) -> None:
        """
        Remove files or directories. Supports: -f -i -v -r -h
        """
        for target in args.targets:
            path = Path(target)
            if not path.exists():
                self._report_error(f"rm: cannot remove '{target}'; No such file or directory", args)
                continue

            if path.is_dir() and not args.recursive:
                self._report_error(f"rm: cannot remove '{target}: Is a directory", args)

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
                    if not self._interactive('rm: Remove', item, args ):
                        continue
                    if item.is_dir():
                        item.rmdir()
                    else:
                        item.unlink()

                    self._verbose(f"rm: Removed {item}", args)

                except PermissionError:
                    self._report_error(f"rm: Permission denied: {item}", args)

                except Exception as e:
                    self._report_error(f"rm: {e}", args)



    @with_argparser(touch_parser)
    def do_touch(self, args: Namespace) -> None:
        """
        Create one or more files. Supports: -f -i -v
        """
        for file in args.path:
            if not self._interactive("touch: Create",file,args):
                continue
            try:
                Path(file).touch(exist_ok=True)
                self._verbose(f"touch: Created {file}", args)

            except PermissionError:
                self._report_error(f"touch: Permission denied: {file}", args)
            except Exception as e:
                self._report_error(f"touch: {e}", args) 

    @with_argparser(pwd_parser)
    def do_pwd(self, args: Namespace) -> None:
        """
        Displays current working directory. Supports: -h
        """
        self.poutput(Path.cwd())
    

    @with_argparser(ls_parser)
    def do_ls(self,args: Namespace) -> None:
        """
        List contents of a directory. Supports: -f -a -h
        """ 
        try:
            entries =  []
            path = Path(args.path)

            for entry in sorted(p for p in path.iterdir() if args.all or not p.name.startswith('.')):

                name = f"{entry.name}/" if entry.is_dir() else entry.name
                entries.append(name)

            self.poutput(" ".join(entries))

        except FileNotFoundError:
            self._report_error(f"ls: No such file or Directory {args.path}", args)
        except Exception as e:
            self._report_error(f"ls: {e}", args)

    
    def _report_error(self,message: str, args: Namespace):
        """
        Write out error messages
        """
        if not args.force:
            self.perror(message)
    
    def _interactive(self,action:str, item: Path, args: Namespace) -> bool:
        """
        Ask for confirmation before each action
        """
        if args.interactive:
            response = input(f"{action}: '{item}'? (y/n) ").strip().lower()
            return response == 'y'
        return True

    def _verbose(self, message:str, args: Namespace):
        """
        Displays information about each action
        """
        if args.verbose:
            self.poutput(message)



if __name__ == "__main__":
    ZenShell().cmdloop()
