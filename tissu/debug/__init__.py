from fabric.api import puts, env, task
from fabric.colors import yellow

@task 
def print_env():
    for k,v in env.items():
        puts("%s : %s" % ( yellow(k),v ) )