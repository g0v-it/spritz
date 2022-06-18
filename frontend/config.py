# import os.path
import os

#BASEPATH = os.path.join("/opt","voting")
#BINPATH = os.path.join(BASEPATH, "bin")
#ELECTIONPATH = os.path.join(BASEPATH,"elections")

#
# Database configuration
#
# DBTYPE="postgresql"   #   deprecated
DBHOST  = os.environ.get('SPRITZ_DBHOST') # "localhost"
DBNAME  = os.environ.get('SPRITZ_DBNAME') # "spritz"
DBUSER  = os.environ.get('SPRITZ_DBUSER') # "dinogen"
DBPWD   = os.environ.get('SPRITZ_DBPWD')  # "abc123"
DBPORT  = os.environ.get('SPRITZ_DBPORT') # 3306
#SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DBUSER,DBPWD,DBHOST,5432,DBNAME)
SQLALCHEMY_DATABASE_URI='mysql://{}:{}@{}:{}/{}'.format(DBUSER,DBPWD,DBHOST,DBPORT,DBNAME)
#SQLALCHEMY_DATABASE_URI='sqlite:///test.db'

#
# Authentication
#
#AUTH = 'test' # fake login base on voting_user sql table, testing pourpose
# AUTH = 'ldap' # ldap auth
# AUTH = 'google' # google auth
# AUTH = 'superauth' # www.superauth.com
# AUTH = 'auth0' # auth0.com
# AUTH = os.environ.get('SPRITZ_AUTH')
AUTH = os.environ.get('SPRITZ_AUTH')

#
# Global variables
#
db = None
app = None

# Constants, do not edit
MSG_INFO = 0
MSG_OK   = 1
MSG_KO   = 2
