"""Authentication module for LDAP
"""
import os
import ldap

LDAP_SERVER_HOST = os.environ.get('LDAP_SERVER_HOST') # ldap.forumsys.com
LDAP_SERVER_PORT = os.environ.get('LDAP_SERVER_PORT') # 389
LDAP_USER_SEARCH_BASE = os.environ.get('LDAP_USER_SEARCH_BASE') # dc=example,dc=com
#LDAP_ROOT_DN = os.environ.get('LDAP_ROOT_DN') 
LDAP_USER_SEARCH_FILTER = os.environ.get('LDAP_USER_SEARCH_FILTER') # uid={}

LDAP_URL = "ldap://{}:{}/".format(LDAP_SERVER_HOST,LDAP_SERVER_PORT) # ldap://ldap.forumsys.com:389/
LDAP_BIND = "{},{}".format(LDAP_USER_SEARCH_FILTER, LDAP_USER_SEARCH_BASE) # uid={},dc=example,dc=com

#print(LDAP_URL, LDAP_BIND)

#LDAP_URL = 'ldap://ldap.forumsys.com:389/'
# if this is true, an unknown username is added in the internal database
# at the first login, if the login is successful
ADD_UNKNOWN_USER=True

def get_ldap_connection():
    conn = ldap.initialize(LDAP_URL)
    return conn

def auth(user_name,token):
    try: 
        conn = get_ldap_connection()
        conn.simple_bind_s(LDAP_BIND.format(user_name),token)
        return True
    except:
        return False
    return False


