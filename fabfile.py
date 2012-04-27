import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


from fabric.api import *
from backupator.api import *

#e("hacksxb")

@task
@roles("all")
def test():
    run("uptime")

