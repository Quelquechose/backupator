import os

from fabric.api import *
from fabric.colors import red
from backupator.api import get_backupator_root, get_backup_dir
from backupator.conf import settings

@task 
@roles('node')
def setup():
    backupator_root = get_backupator_root()
    backup_dir = get_backup_dir()

    if backup_dir is not None:
        run("mkdir -p %s" % (backup_dir,))
    else:
        abort(red("The backup_dir is not set in %s hostdef" % (hostdef.get("hostname"))))

    if backupator_root is not None:
        run("mkdir -p %s" % (backupator_root, ))
        with cd(backupator_root):
            run("rm -rf src env")
            run("virtualenv --no-site-package env")
            run("git clone git@github.com:Quelquechose/backupator.git src")
            with prefix("source env/bin/activate"):
                run("pip install -r src/requirements.txt")

    else:
        abort(red("The backupator_root is not set in %s hostdef" % (hostdef.get("hostname"))))

@task
@roles('node')
def update_env():
    with cd(get_backupator_root()):
        with prefix("source env/bin/activate"):
            run("pip install -U -r src/requirements.txt")

@task()
@roles('node')
def update_code():
    with cd(get_backupator_root()):
        with cd("src"):
            run("git pull")

@task
@roles('node')
def cleanup():
    with cd(get_backupator_root()):
        run("find . -name \"*.pyc\" -exec rm -f '{}' ';'")

@task()
@roles('node')
def update():
    execute(update_env)
    execute(update_code)
    execute(cleanup)


@task
@roles('node')
def launch(command):
    with cd(get_backupator_root()):
        with cd("src"):
            with prefix("source ../env/bin/activate"):
                run(command)

@task
@roles('node')
def upload(filepath):
    from backupator.conf import settings

    local_path = "%s/%s" % (getattr(settings, "PROJECT_PATH"), filepath)
    remote_path = "%s/%s/%s" % (get_backupator_root(), "src", filepath)
    
    put(local_path, remote_path)

@task
@roles('node')
def uptime():
    run("uptime")