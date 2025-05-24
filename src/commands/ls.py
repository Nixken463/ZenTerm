from argparse import Namespace
from pathlib import Path
import stat
import os
from datetime import datetime
import platform
if platform.system() != "Windows":
    import pwd
    import grp


def execute_ls(self,args: Namespace) -> None:
        try:
            path = Path(args.path)
            entries = create_sort_list(path, args)
            if not args.long:
                if args.s or args.S:
                    entries_with_size = []
                    for entry in entries:
                        entry_path = path / entry
                        size = f"{entry_path.stat().st_size:>8}"
                        entries_with_size.append(f"{size} {entry}")
                    self.poutput(" ".join(entries_with_size))
                else:
                    self.poutput(" ".join(entries))
            elif args.long and platform.system() != "Windows":
                for entry in entries:
                    path = Path(entry)
                    stats =  get_stats(path) 
                    link_count = get_link_count(path)
                    modify_time = get_modify_time(path) 
                    owner, group = get_owner_group(path)
                    size = f"{path.stat().st_size:>8}" if args.s or args.S else "" 
                    self.poutput(f"{stats} {link_count:>3} {owner} {group} {size} {modify_time} {entry}")

            if args.long and platform.system() == "Windows": 
                self.poutput("ls: -l is currently only supported on Linux")
        except FileNotFoundError:
            self.report_error(f"ls: No such file or Directory {args.path}", args)
        except Exception as e:
            self.report_error(f"ls: {e}", args)


def get_stats(path: Path) -> str:
    is_dir = 'd' if path.is_dir() else '-'
    mode = path.stat().st_mode
    
    perms = [
        (stat.S_IRUSR, 'r'), (stat.S_IWUSR, 'w'), (stat.S_IXUSR, 'x'),
        (stat.S_IRGRP, 'r'), (stat.S_IWGRP, 'w'), (stat.S_IXGRP, 'x'),
        (stat.S_IROTH, 'r'), (stat.S_IWOTH, 'w'), (stat.S_IXOTH, 'x')]
    perm_str = ''.join(char if mode & flag else '-' for flag, char in perms)
    stats = is_dir + perm_str
    return stats


def get_link_count(path: Path) -> int:
    if path.is_dir():
        link_count = 2
        with os.scandir(path) as scan:
            for entry in scan:
                if entry.is_dir(follow_symlinks=False):
                    link_count += 1
                else:
                    continue
        return link_count
    else:
        return path.stat().st_nlink

def get_modify_time(path: Path) -> str:
    unix_time = os.path.getmtime(path)
    readable_time= datetime.fromtimestamp(unix_time).strftime('%b %d %H:%M')
    return readable_time

def get_owner_group(path: Path) -> tuple:
    stat_info = path.stat()
    user = pwd.getpwuid(stat_info.st_uid).pw_name
    group = grp.getgrgid(stat_info.st_gid).gr_name
    return user, group


def create_sort_list(path: Path, args) -> list:

        entries = sorted([p for p in path.iterdir() if args.all or not p.name.startswith('.')])
        if args.S:
            entries = sorted(entries, key=lambda f: f.stat().st_size)
            entries.reverse()
        if args.reverse:
            entries.reverse()
        names = [f"{entry.name}/" if entry.is_dir() else entry.name for entry in entries]
        return names
