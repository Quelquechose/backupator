from fabric.api import *
from backupator.api import lrun, get_backup_dir

@roles('files')
@task
def backup():
    lrun("whoami")