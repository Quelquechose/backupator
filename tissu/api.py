import os

from fabric.api import env, run
from fabric.context_managers import settings
from fabric.decorators import task, roles
from fabric.colors import red, green, magenta, yellow
from fabric.operations import open_shell
from fabric.utils import abort, puts, warn


os.environ['APP_SETTINGS_MODULE'] = 'settings.default'

def set_settings_module(envname):
    """
    Load the settings module for a specific environement name
    """
    filename = "%s.py" % envname
    if os.path.exists(os.path.join(".", "settings", filename)):
        os.environ['APP_SETTINGS_MODULE'] = "settings.%s" % envname
        return True
    else:
        return False

def set_roledefs():
    """
    Load the cluster nodes roles in the fabric env
    """
    from backupator.conf import settings
    roledefs = getattr(settings, 'APP_ROLEDEFS', None)
    
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
    env.parallel = settings.FABRIC_PARALLEL_EXECUTION
    env.pool_size = settings.FABRIC_PARALLEL_POOLSIZE


def host_string(username, hostname):
    return "%s@%s" % (username, hostname)


def hoststring_from_hostdef(h):
    return host_string(h.get('user'), h.get('hostname'))

def epy(envname=None):
    """
    Load fabric env from python settings files
    """
    if set_settings_module(envname) is False:
         abort(red("Unable to find  %s settings" % envname))
         return False

    from backupator.conf import settings

    roledefs = getattr(settings, 'APP_ROLEDEFS', {})
    
    all_hosts = []
    setattr(env, "hostdefs", {})

    for role,hosts in roledefs.items():
        role_hosts = [ hoststring_from_hostdef(h) for h in hosts]
        all_hosts += role_hosts
        env.roledefs[role] = role_hosts
        
        password = dict((hoststring_from_hostdef(h), h.get("password")) for h in hosts)
        env.passwords.update(password)        

        hostdefs = dict((hoststring_from_hostdef(h), h) for h in hosts)
        env.hostdefs.update(hostdefs)

        key = [ h.get("key") for h in hosts]
        if env.key_filename is None:
            env.key_filename = key
        else:
            env.key_filename += key
    
    env.roledefs['all'] = list(set( all_hosts ))
    
    if len(env.roledefs) == 0:
         abort(red("Unable to load ROLEDEFS is APP_ROLEDEFS defined in your settings file ?"))
    else:
        set_parallel_execution()
        
        puts(green("Environment %s sucessfully loaded :)" % envname))



def eini(envname):
    """
    Load fabric env from ini files
    """
    raise NotImplementedError()


def get_hostdef(host_string):
    return env.hostdefs.get(host_string, {})


def current_hostdef():
    return get_hostdef(env.host_string)



ENV_LOADER_PYTHON = "python"
ENV_LOADER_INI = "ini"


ENV_LOADERS = {
    ENV_LOADER_PYTHON : epy,
    ENV_LOADER_INI : eini,
}

@task
def l(loader):
    if loader in ENV_LOADERS.keys():
        env.tissu_loader = loader
    else:
        abort(red("%s is not a valider loader name, accepted values are : %s" % (loader, ENV_LOADERS.keys())))

@task
def e(envname):
    loader = getattr(env,"tissu_loader" , ENV_LOADER_PYTHON)
    
    if envname is not None:
        ENV_LOADERS[loader](envname)
    else:
        abort(red("Please give an environment name :( \n$ fab e:production"))
