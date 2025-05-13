import os, sys
from cmd2 import Cmd



print("""

███████╗███████╗███╗░░██╗████████╗███████╗██████╗░███╗░░░███╗
╚════██║██╔════╝████╗░██║╚══██╔══╝██╔════╝██╔══██╗████╗░████║
░░███╔═╝█████╗░░██╔██╗██║░░░██║░░░█████╗░░██████╔╝██╔████╔██║
██╔══╝░░██╔══╝░░██║╚████║░░░██║░░░██╔══╝░░██╔══██╗██║╚██╔╝██║
███████╗███████╗██║░╚███║░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
╚══════╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝

""")


class ZenShell(Cmd):
        
    @property
    def prompt(self):
        return f"{os.path.basename(os.getcwd())} "


    def do_cd(self, path):
            try:
                os.chdir(os.path.abspath(path))
            except:
                self.perror(f"cd: No such file or directory: {path}")

    def do_exit(self, _):
        return True
    

    def do_pwd(self, _):
        print(os.getcwd())



if __name__ == "__main__":
    ZenShell().cmdloop()
