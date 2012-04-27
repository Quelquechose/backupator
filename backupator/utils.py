from datetime import datetime

from fabric.api import env, run
from fabric.context_managers import settings
from fabric.decorators import task, roles
from fabric.colors import red, green
from fabric.operations import open_shell, put, get
from fabric.utils import abort, puts
from fabric.tasks import execute


@task
def shell():
    """
    Launch a shell on a specific host, because sometimes you need it quickly !
    """
    open_shell()

@task
@roles('all')
def quick_run(command):
    """
    Fire, aime, repeat !
    """
    run(command)

@task
def disable_parallel():
    """
    Disable all paralell call 
    """
    env.parallel = False
    
@task
@roles('all')
def uptime():
    """
    Because uptime is sooo important
    """
    run("uptime")


@task
@roles('all')
def upload(local_path, remote_path):
    """
    On peut filter avec les kwargs fabric des taks : 
    host=None, hosts=None, role=None, roles=None, exclude_hosts=None
    """
    put(local_path, remote_path)


@task
@roles('all')
def download(remote_path, local_path="./tmp"):
    get(remote_path, local_path)



