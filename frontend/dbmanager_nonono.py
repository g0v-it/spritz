# ignore this file, it is sometime useful...
import config
if config.DBTYPE == 'postgresql':
    import psycopg2 as db
    from psycopg2.extras import DictCursor

def get_connection():
    if config.DBTYPE == 'postgresql':
        conn = db.connect(host=config.DBHOST,dbname=config.DBNAME, \
        user=config.DBUSER, password=config.DBPWD, cursor_factory=DictCursor)
        conn.set_session(autocommit=True) # to be fixed
    return conn
