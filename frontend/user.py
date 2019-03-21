import dbmanager
import config
from flask_login import UserMixin
if config.AUTH == 'ldap':
    import auth_ldap as auth
if config.AUTH == 'google':
    import auth_google as auth
    
class user_dto:
    """This class is a DTO for the database table"""
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.pass_word = None
        
class User(UserMixin):
    """This class is for the Flask-login session"""
    def __init__(self, user_name=''):
        self.user_name = user_name
        self.u = load_user_by_username(user_name)    
    def get_id(self):
        return str(self.user_name) # must be unicode
    def try_to_authenticate(self, pass_word):
        if self.u:
            return auth.auth(self.user_name, pass_word)
        return False
    def is_valid(self):
        return self.u != None


def load_user_by_id(user_id):
    """Returns a user_dto object or None"""
    u = None
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from voting_user where user_id = %s", (user_id,) )
    row = c.fetchone()
    if row:
        u = user_dto()
        u.user_id = row['user_id']
        u.user_name = row['user_name']
        u.pass_word = row['pass_word']
    c.close()
    conn.close()
    return u

def load_user_by_username(user_name):
    """Returns a user_dto object or None"""
    u = None
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from voting_user where user_name = %s", (user_name,) )
    row = c.fetchone()
    if row:
        u = user_dto()
        u.user_id = row['user_id']
        u.user_name = row['user_name']
        u.pass_word = row['pass_word']
    c.close()
    conn.close()
    if auth.ADD_UNKNOWN_USER:
        if u == None:
            u = user_dto()
            u.user_name = user_name
            u.pass_word = 'new user'
            insert_user_dto(u)
    return u

def delete_user_by_id(user_id):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from voting_user where user_id = %s", (user_id,) )
    c.close()
    conn.close()

def delete_user_by_username(user_name):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from voting_user where user_name = %s", (user_name,) )
    c.close()
    conn.close()

def insert_user_dto(u):
    conn = dbmanager.get_connection()
    c = conn.cursor()

    if config.DBTYPE == 'sqlite3':
        c.execute("insert into voting_user(user_name,pass_word) values(%s,%s)", (u.user_name,u.pass_word))
        u.user_id = c.lastrowid
    if config.DBTYPE == 'postgresql':
        c.execute("insert into voting_user(user_name,pass_word) values(%s,%s) returning user_id", (u.user_name,u.pass_word))
        row =c.fetchone()
        u.user_id = row[0]

    c.close()
    conn.close()
