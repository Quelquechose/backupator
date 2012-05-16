from fabric.api import *
from backupator.api import run

@roles('files')
@task
def test():
    run("whoami")