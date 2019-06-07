import os.path
import os
SECRET_KEY = b'Live long and prosper' # you really should change this, according to Flask user guide
BASEPATH = os.path.join("/opt","voting")
DBTYPE="postgresql"
#DBPATH = os.path.join(BASEPATH, "database","copernico-spritz.sqlite3.db") # deprecated
DBHOST = os.environ.get('POSTGRES_HOST')   # "localhost"
DBNAME = os.environ.get('POSTGRES_DBNAME') # "spritz"
DBUSER = os.environ.get('POSTGRES_USER')   # "dinogen"
DBPWD  = os.environ.get('POSTGRES_PWD')    # "abc123"
BINPATH = os.path.join(BASEPATH, "bin")
ELECTIONPATH = os.path.join(BASEPATH,"elections")
# AUTH = 'ldap'
AUTH = 'google'
# AUTH = 'test' # fake login base on voting_user sql table, testing pourpose
# AUTH = os.environ.get('SPRITZ_AUTH')
