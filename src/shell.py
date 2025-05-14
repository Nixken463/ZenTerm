#Made by Nixken
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
# add option for passing a dir, like ls src or ls ZenTerm/src
    def do_ls(self, _):
        try:
            entries =  []
            path = os.getcwd()
            for entry in sorted(os.listdir()):
                name = entry + "/" if os.path.isdir(path + "/" + entry) else entry
                entries.append(name)

            print(" ".join(entries))

        except Exception as e:
            print(f"Error: {e}")
if __name__ == "__main__":
    ZenShell().cmdloop()
