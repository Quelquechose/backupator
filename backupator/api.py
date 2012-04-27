import os

from fabric.api import env, run
from fabric.context_managers import settings
from fabric.decorators import task, roles
from fabric.colors import red, green, magenta
from fabric.operations import open_shell
from fabric.utils import abort, puts, warn

import db

os.environ['RBSCOOKING_SETTINGS_MODULE'] = 'settings.default'

def set_settings_module(envname):
    """
    Load the settings module for a specific environement name
    """
    filename = "%s.py" % envname
    if os.path.exists(os.path.join(".", "settings", filename)):
        os.environ['RBSCOOKING_SETTINGS_MODULE'] = "settings.%s" % envname
        return True
    else:
        return False

def set_roledefs():
    """
    Load the cluster nodes roles in the fabric env
    """
    from backupator.conf import settings
    roledefs = getattr(settings, 'WEBAPP_ROLEDEFS', None)
    
    if roledefs is None or roledefs == {}:
        return False

    hosts = []
    for role in roledefs.keys():            
        hosts = hosts + roledefs[role]  
    
    roledefs['all'] = list(set(hosts))
    env.roledefs.update( roledefs )
    return True


def set_parallel_execution():
    from backupator.conf import settings
    env.parallel = settings.RBS_COOKING_PARALLEL_EXECUTION
    env.pool_size = settings.RBS_COOKING_PARALLEL_POOLSIZE


def host_string(username, hostname):
    return "%s@%s" % (username, hostname)


def hoststring_from_hostdef(h):
    return host_string(h.get('user'), h.get('hostname'))


def eproto(envname=None):
    """
    Load fabric env from our first way of settings
    this loader is for retro compatifibility
    """

    if envname is not None:
        if set_settings_module(envname) is False:
             abort(red("Unable to find  %s settings" % envname))
             return False

        if set_roledefs() is False:
             abort(red("Unable to load ROLEDEFS is WEB_APP_ROLEDEFS defined in your settings file ?"))

        set_parallel_execution()
        
        from backupator.conf import settings
    
        
        if settings.WEBAPP_SSH_USER is not None:
            env.user = settings.WEBAPP_SSH_USER
        else:
            abort(red("ERROR Environment %s not found :(" % envname))


        if getattr(settings, 'WEBAPP_SSH_KEY', None) is not None:
            env.key_filename = settings.WEBAPP_SSH_KEY
        
        if getattr(settings, 'WEBAPP_SSH_PASSWORD', None) is not None:
            env.password = settings.WEBAPP_SSH_PASSWORD
    
        puts(green("Environment %s sucessfully loaded :)" % envname))
    else:
        abort(red("Please give an environment name :( \n$ fab e:production"))


def epy(envname=None):
    """
    Load fabric env from python settings files
    """
    if set_settings_module(envname) is False:
         abort(red("Unable to find  %s settings" % envname))
         return False

    from backupator.conf import settings

    roledefs = getattr(settings, 'WEBAPP_ROLEDEFS', {})
    
    all_hosts = []
    
    for role,hosts in roledefs.items():
        role_hosts = [ hoststring_from_hostdef(h) for h in hosts]
        all_hosts += role_hosts
        env.roledefs[role] = role_hosts
        
        
        password = dict((hoststring_from_hostdef(h), h.get("password")) for h in hosts)
        env.passwords.update(password)
    
        key = [ h.get("key") for h in hosts]
        if env.key_filename is None:
            env.key_filename = key
        else:
            env.key_filename += key
    
    env.roledefs['all'] = list(set( all_hosts ))
    
    if len(env.roledefs) == 0:
         abort(red("Unable to load ROLEDEFS is WEB_APP_ROLEDEFS defined in your settings file ?"))
    else:
        set_parallel_execution()
        puts(green("Environment %s sucessfully loaded :)" % envname))

def eini(envname):
    """
    Load fabric env from ini files
    """
    raise NotImplementedError()



ENV_LOADER_PROTO_PYTHON = "proto_python"
ENV_LOADER_PYTHON = "python"
ENV_LOADER_INI = "ini"


ENV_LOADERS = {
    ENV_LOADER_PROTO_PYTHON : eproto,
    ENV_LOADER_PYTHON : epy,
    ENV_LOADER_INI : eini
}


@task
def l(loader):
    if loader in ENV_LOADERS.keys():
        env.rbscooking_loader = loader
    else:
        abort(red("%s is not a valider loader name, accepted values are : %s" % (loader, ENV_LOADERS.keys())))

@task
def e(envname):
    loader = getattr(env,"rbscooking_loader" , ENV_LOADER_PYTHON)
    
    if envname is not None:
        ENV_LOADERS[loader](envname)
    else:
        abort(red("Please give an environment name :( \n$ fab e:production"))


def mkdir(path, no_parents_error=True):
    basecmd = "mkdir"
    if no_parents_error is True:
        basecmd = "%s -p" % basecmd
    run("%s %s" % (basecmd, path))

def symlink(src, dest, options="-nsf"):
    run("ln %s %s %s" % (options,src,dest))


