import os.path

from datetime import datetime

from fabric.api import *
from fabric.colors import red
from fabric.operations import get
from fabric.contrib import files

from backupator.conf import settings
from backupator.api import lrun, get_backup_dir, current_hostdef

def get_settings():
    hostdef = current_hostdef()
    mysql = hostdef.get("mysql")

    user = mysql.get("user")
    passwd = mysql.get("passwd")
    host = mysql.get("host", "localhost")
    ignore = mysql.get("ignore_database", [])
    return (user, passwd, host, ignore)

@task
@roles("mysql")
def dump( dbname, user, passwd, host="localhost"):
    filename = "~/%s_%s.sql" % (dbname, datetime.now().strftime("%Y%m%d_%H%M%S") )
    lrun("mysqldump -h %s -u %s -p%s %s > %s" % (host, user, passwd, dbname, filename))
    
    destination = "%s/mysql/" % (get_backup_dir(),)
    if not os.path.exists(destination):
         lrun("mkdir -p %s" % (destination,))

    get(filename, destination)
    lrun("rm %s" % filename)

@task
@roles("mysql")
def get_names(user, passwd, host="localhost", ignore=None):
    cmd = "mysql -u%s -p%s --batch -e \"SHOW DATABASES\" -h %s" % (user, passwd, host)
    output = run(cmd)
    db_names = output.split("\r\n")[1:]
    if ignore is not None:
        for name in ignore:
	    print name, db_names
	    db_names.remove(name)
    return db_names

@task
@roles("mysql")
def backup():    
    user, passwd, host, ignore = get_settings()

    if user:
    	db_names = get_names(user, passwd, host, ignore)

        for db_name in db_names:
	       dump(db_name, user, passwd, host)

    else:
        warn(red("Impossible de charger les settings MySQL")) 





