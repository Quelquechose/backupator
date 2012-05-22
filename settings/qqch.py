from default import *

DEBUG = True



FABRIC_PARALLEL_EXECUTION = False

MYSQL = {
 "host" : "localhost",
 "user" : "hacksxb",
 "passwd" : "xxxx",
 "ignore_database": ["information_schema",],
}



VALKYRIE2= {
 "hostname" : "valkyrie2", 
 "user" : "jeanglode",
 "backupator_root" : "~/backupator",
 "backup_dir" : "~/backup/",
 "mysql" : MYSQL,
}

LOCALHOST = {
 "hostname" : "localhost",
 "force_local" : True,
}


APP_ROLEDEFS = {
    'mysql': [VALKYRIE2, LOCALHOST],
    'files': [VALKYRIE2, LOCALHOST],
    'node' : [VALKYRIE2]
}




BACKUP_PROCESS = {
    #"db.mysql",
    "files"
}

try:
    from local_settings import *
except ImportError, exp:
    pass