
DEBUG = True


VALKYRIE2= {
 "hostname" : "xxxx", 
 "user" : "xxxx",
 "password": "xxxx"
}

SOULOU= {
 "hostname" : "xxx",
 "user" : "xxxx",
 "password" : "xxxx"
}

WEBAPP_ROLEDEFS = {
    'mysql': [VALKYRIE2],
    'pgsql': [SOULOU],
}

MYSQL = {
 "host" : "localhost",
 "user" : "hacksxb",
 "passwd" : "xxxx",
 "ignore_database": ["information_schema",],
}

PGSQL = {
 "host" : "localhost",
 "user" : "backup_pgsql",
 "passwd" : "hacksxb67",
 "ignore_database": ["template0"],
}

BACKUP = {
 "repo_path": "~/backup/repo",
}

