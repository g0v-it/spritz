"""Authentication module for LDAP
"""
import ldap

LDAP_URL = 'ldap://ldap.forumsys.com:389/'
# if this is true, an unknown username is added in the internal database
# at the first login, if the login is successful
ADD_UNKNOWN_USER=True

def get_ldap_connection():
    conn = ldap.initialize(LDAP_URL)
    return conn

def auth(user_name,token):
    try: 
        conn = get_ldap_connection()
        conn.simple_bind_s('uid={},dc=example,dc=com'.format(user_name),token)
        return True
    except:
        return False
    return False


