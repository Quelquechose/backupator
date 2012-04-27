import os.path

from datetime import datetime

from fabric.api import *
from fabric.colors import red
from fabric.operations import get
from fabric.contrib import files


from backupator.conf import settings




@task
@roles("mysql")
def dump( dbname, user, passwd, host="localhost"):
    filename = "~/%s_%s.sql" % (dbname, datetime.now().strftime("%Y%m%d_%H%M%S") )
    run("mysqldump -h %s -u %s -p%s %s > %s" % (host, user, passwd, dbname, filename))
    
    destination = "%s/mysql/" % (settings.BACKUP["repo_path"],)
    if not os.path.exists(destination):
         run("mkdir -p %s" % (destination,))


    get(filename, destination)
    run("rm %s" % filename)

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
    if hasattr(settings, "MYSQL"):
        
	user = settings.MYSQL["user"]
	passwd = settings.MYSQL["passwd"]
	host = settings.MYSQL.get("host", "localhost")
	ignore = settings.MYSQL["ignore_database"]
	db_names = get_names(user, passwd, host, ignore)

        for db_name in db_names:
	    dump(db_name, user, passwd, host)


    else:
        warn(red("Impossible de charger les settings MySQL")) 





