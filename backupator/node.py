
from fabric.api import *
from fabric.colors import red
from backupator.api import get_backupator_root
from backupator.conf import settings

@task 
@roles('node')
def setup():
    backupator_root = get_backupator_root()
    if backupator_root is not None:
        run("mkdir -p %s" % (backupator_root, ))
        with cd(backupator_root):
            run("rm -rf src env")
            run("virtualenv --no-site-package env")
            run("git clone git@github.com:Quelquechose/backupator.git src")
            run("pip install -r src/requirements.txt")

    else:
        abort(red("The backupator_root is not set in %s hostdef" % (hostdef.get("hostname"))))

@task
@roles('node')
def update_env():
    with cd(get_backupator_root()):
        with prefix("source env/bin/activate"):
            run("pip install -U -r src/requirements.txt")

@task
@roles('node')
def cleanup():
    with cd(get_backupator_root()):
        run("find . -name \"*.pyc\" -exec rm -f '{}' ';'")

@task()
@roles('node')
def update():
    execute(update_env)
    with cd(get_backupator_root()):
        with cd("src"):
            run("git pull")
    execute(cleanup)

@task
@roles('node')
def launch(command):
    with cd(get_backupator_root()):
        with cd("src"):
            with prefix("source ../env/bin/activate"):
                run(command)
