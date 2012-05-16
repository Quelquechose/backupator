import os

from fabric.api import env, abort
from fabric.api import run as fabric_run
from fabric.api import local as fabric_local

from fabric.context_managers import settings
from fabric.decorators import task, roles
from fabric.colors import red, green, magenta
from fabric.operations import open_shell
from fabric.utils import abort, puts, warn

from tissu.api import *
from tissu.api import e as __e
from tissu import importlib
from fabric.main import load_tasks_from_module
from fabric import state


@task
def e(env_name):
    __e(env_name)
    from backupator.conf import settings
    for app in getattr(settings, "BACKUP_APPS", None):
        if app is not None:
            try:
                imported = importlib.import_module(app)
                print imported
                # Actually load tasks
                docstring, new_style, classic, default = load_tasks_from_module(imported)
                print docstring, new_style, classic, default
                tasks = new_style if state.env.new_style_tasks else classic
                print tasks

                state.commands.update(tasks)


            except ImportError, err:
                abort(red("Could not import backup application '%s' (Is it on sys.path?): %s" % (app, err)))


def run(cmd):
    """
    local or remote run
    """
    force_local = current_hostdef().get("force_local", False)
    if force_local:
        return fabric_local(cmd)
    else:
        return fabric_run(cmd)

