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
LOGIN_TEMPLATE = 'login_template.html'
CLIENT_ID = ''

#print(LDAP_URL, LDAP_BIND)

#LDAP_URL = 'ldap://ldap.forumsys.com:389/'
# if this is true, an unknown username is added in the internal database
# at the first login, if the login is successful
ADD_UNKNOWN_USER=True

def get_ldap_connection():
    conn = ldap.initialize(LDAP_URL)
    return conn

def get_auth_data(request):
    user_name = request.form['user_name']
    pass_word = request.form['pass_word']
    auth_data = {'username': user_name, 'password': pass_word}
    return auth_data

def auth(auth_data):
    message = 'Login failed'
    return_code = False
    user_name = auth_data['username']
    try: 
        conn = get_ldap_connection()
        conn.simple_bind_s(LDAP_BIND.format(auth_data['username']),auth_data['password'])
        return_code = True
        message = 'Login successful'
    except:
        return_code = False
        message = 'Wrong user or password'
    auth_result = {'username': user_name, 'message': message, 'logged_in': return_code}
    return auth_result


