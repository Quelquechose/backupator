import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


from fabric.api import *
from backupator.api import *

import tissu.debug as debug
from backupator import db, files, node


