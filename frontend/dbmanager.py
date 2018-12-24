import config
if config.DBTYPE == 'sqlite3':
    import sqlite3 as db
if config.DBTYPE == 'postgresql':
    import psycopg2 as db
    from psycopg2.extras import DictCursor

def get_connection():
    if config.DBTYPE == 'sqlite3':
        conn = db.connect(config.DBPATH)
        conn.row_factory = db.Row
        conn.isolation_level = None # no commit needed
    if config.DBTYPE == 'postgresql':
        conn = db.connect(host=config.DBHOST,dbname=config.DBNAME, \
        user=config.DBUSER, password=config.DBPWD, cursor_factory=DictCursor)
        conn.set_session(autocommit=True)
    return conn
