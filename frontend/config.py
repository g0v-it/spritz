import os.path
import os

#BASEPATH = os.path.join("/opt","voting")
#BINPATH = os.path.join(BASEPATH, "bin")
#ELECTIONPATH = os.path.join(BASEPATH,"elections")

#
# Database configuration
#
DBTYPE="postgresql"
DBHOST = os.environ.get('POSTGRES_HOST')   # "localhost"
DBNAME = os.environ.get('POSTGRES_DBNAME') # "spritz"
#DBNAME = "prova" # just a test
DBUSER = os.environ.get('POSTGRES_USER')   # "dinogen"
DBPWD  = os.environ.get('POSTGRES_PWD')    # "abc123"
SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DBUSER,DBPWD,DBHOST,5432,DBNAME)
#SQLALCHEMY_DATABASE_URI='sqlite:///test.db'

#
# Authentication
#
# AUTH = 'ldap' # ldap auth
AUTH = 'google' # google auth
# AUTH = 'superauth' # www.superauth.com
# AUTH = 'test' # fake login base on voting_user sql table, testing pourpose
# AUTH = os.environ.get('SPRITZ_AUTH')

#
# Global variables
#
db = None

# Constants, do not edit
MSG_INFO = 0
MSG_OK   = 1
MSG_KO   = 2
