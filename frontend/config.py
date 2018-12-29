import os.path
SECRET_KEY = b'il mio cuore'
BASEPATH = os.path.join("/opt","voting")
DBTYPE="postgresql"
DBPATH = os.path.join(BASEPATH, "database","copernico-spritz.sqlite3.db")
DBHOST = "localhost"
DBNAME = "spritz"
DBUSER = "dinogen"
DBPWD = "abc123"
BINPATH = os.path.join(BASEPATH, "bin")
ELECTIONPATH = os.path.join(BASEPATH,"elections")
