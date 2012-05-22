import os

from fabric.api import *
from tissu.api import *


def lrun(cmd):
    """
    local or remote run
    """
    force_local = current_hostdef().get("force_local", False)
    if force_local:
        return local(cmd)
    else:
        return run(cmd)

def get_backupator_root():
    return current_hostdef().get("backupator_root", None)

@task
def backup():
    from backupator.conf import settings
    for process_task in getattr(settings,"BACKUP_PROCESS", []):
        execute("%s.backup" % (process_task,))