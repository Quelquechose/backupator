
DEBUG = True


FABRIC_PARALLEL_EXECUTION = False

VALKYRIE2= {
 "hostname" : "valkyrie2", 
 "user" : "jeanglode",
}

LOCALHOST = {
 "hostname" : "localhost",
 "force_local" : True,
}


APP_ROLEDEFS = {
    'mysql': [VALKYRIE2, LOCALHOST],
    'files': [VALKYRIE2, LOCALHOST],
}

MYSQL = {
 "host" : "localhost",
 "user" : "hacksxb",
 "passwd" : "xxxx",
 "ignore_database": ["information_schema",],
}


BACKUP = {
 "repo_path": "~/backup/repo",
}

BACKUP_APPS = {
    "backupator.db.mysql",
    "backupator.files"
}
