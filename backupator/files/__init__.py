from fabric.api import *
from backupator.api import lrun

@roles('files')
@task
def backup():
    lrun("whoami")