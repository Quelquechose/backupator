import os

from fabric.api import *
from tissu.api import *

def is_force_local():
    return current_hostdef().get("force_local", False)


def lrun(cmd):
    """
    local or remote run
    """
    if is_force_local():
        return local(cmd, capture=True)
    else:
        return run(cmd)    

def get_backupator_root():
    return current_hostdef().get("backupator_root", None)

def get_backup_dir():
    return current_hostdef().get("backup_dir", None)

@task
def backup(*args, **kwargs):
    from backupator.conf import settings

    if len(args) > 0:
        tasks = args
    else:
        tasks = getattr(settings,"BACKUP_PROCESS", [])

    for process_task in tasks:
        execute("%s.backup" % (process_task,))