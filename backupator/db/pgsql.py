from datetime import datetime

import os.path

from fabric.api import *
from fabric.colors import red
from fabric.operations import get
from fabric.contrib import files

from backupator.conf import settings

@task
@roles("pgsql")
def dump( dbname, user, passwd, host="localhost"):
    filename = "~/%s_%s.sql" % (dbname, datetime.now().strftime("%Y%m%d_%H%M%S") )
    with prefix("export PGPASSWORD=%s" % passwd):
        run("pg_dump -U %s -h %s %s > %s" % (user, host, dbname, filename))
    
    destination = "%s/pgsql/" % (settings.BACKUP["repo_path"],)
    print destination
    if not os.path.exists(destination):
        run("mkdir -p %s" % (destination,))

    destination = "%s%s" % (destination,filename)
    get(filename, destination)
    run("rm %s" % filename)

@task
@roles("pgsql")
def get_names(user, passwd, host="localhost", ignore=None):
    with prefix("export PGPASSWORD=%s ; \
                 export PGUSER=%s ; \
                 export PGHOST=%s" % (passwd, user, host)):
        cmd = "echo \"\\l\" | psql postgres | tr -s ' ' | grep -E \"^ [a-z]\" | cut -d' ' -f2"
        output = run(cmd)
    db_names = output.split("\r\n")[1:]
    if ignore is not None:
        for name in ignore:
            print name, db_names
            db_names.remove(name)
    return db_names

@task
@roles("pgsql")
def backup():
    if hasattr(settings, "PGSQL"):    
        user = settings.PGSQL["user"]
        passwd = settings.PGSQL["passwd"]
        host = settings.PGSQL.get("host", "localhost")
        ignore = settings.PGSQL["ignore_database"]
        db_names = get_names(user, passwd, host, ignore)

        for db_name in db_names:
            dump(db_name, user, passwd, host)


    else:
        warn(red("Impossible de charger les settings PostgreSQL")) 

