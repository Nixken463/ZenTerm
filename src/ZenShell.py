#Made by Nixken
import sys
from cmd2 import Cmd, with_argparser
from pathlib import Path
from argparse import Namespace
import types

import parser
import commands 
import helpers



class ZenShell(Cmd):
    def __init__(self):
        super().__init__()
        self.stdout = sys.stdout
        self.interactive = types.MethodType(helpers.interactive, self)
        self.report_error = types.MethodType(helpers.report_error, self)
        self.verbose = types.MethodType(helpers.verbose, self)
        
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

    @with_argparser(parser.cd_parser)
    def do_cd(self, args: Namespace)-> None:
        """
        Change the working directory. Supports: -h
        """
        commands.execute_cd(self, args)


    @with_argparser(parser.exit_parser)
    def do_exit(self, args:Namespace) -> bool:
        """
        Quit the shell. Supports: -h
        """
        return commands.execute_exit(self, args)

    @with_argparser(parser.mv_parser)
    def do_mv(self, args: Namespace) -> None:
        """
        Move files or directories. Supports: -f -r -v -i
        """
        commands.execute_mv(self, args)


    @with_argparser(parser.cp_parser)
    def do_cp(self, args: Namespace) -> None:
        """
        Copy files or directories. Supports: -f -r -v -i
        """
        commands.execute_cp(self, args)



    @with_argparser(parser.clear_parser)
    def do_clear(self, args: Namespace) -> None:
        """
        Clear the contents of the shell. Supports: -h
        """
        self.poutput("\033c")

    @with_argparser(parser.cat_parser)
    def do_cat(self, args: Namespace) -> None:

        """
        Concatenate and display file content. Supports: -f -h
        """
        commands.execute_cat(self, args)



    @with_argparser(parser.echo_parser)
    def do_echo(self, args: Namespace) -> None:
        """
        Echo the given text to standard output
        """
        commands.execute_echo(self, args)


    @with_argparser(parser.mkdir_parser)
    def do_mkdir(self, args:Namespace) -> None:
        """
        Create one or more directories. Supports: -p -r -i -v -f.
        """ 
        
        commands.execute_mkdir(self, args)



    @with_argparser(parser.rm_parser) 
    def do_rm(self, args: Namespace) -> None:
        """
        Remove files or directories. Supports: -f -i -v -r -d -h
        """
        commands.execute_rm(self, args)


    @with_argparser(parser.touch_parser)
    def do_touch(self, args: Namespace) -> None:
        """
        Create one or more files or update timestamps.
        Supports: -f (force), -i (interactive), -v (verbose)
        """
        commands.execute_touch(self, args)


    @with_argparser(parser.pwd_parser)
    def do_pwd(self, args: Namespace) -> None:
        """
        Displays current working directory. Supports: -h
        """
        commands.execute_pwd(self, args)
    
    

    @with_argparser(parser.ls_parser)
    def do_ls(self,args: Namespace) -> None:
        """
        List contents of a directory. Supports: -f -a -l -h
        """ 
        commands.execute_ls(self,args)


if __name__ == "__main__":
    ZenShell().cmdloop()
