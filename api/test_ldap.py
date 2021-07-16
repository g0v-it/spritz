import ldap

def get_ldap_connection():
    conn = ldap.initialize('ldap://ldap.forumsys.com:389/')
    return conn


conn = get_ldap_connection()
#conn.simple_bind_s('cn=%s,ou=Users,dc=testathon,dc=net' % username,password)
#conn.simple_bind_s('cn=read-only-admin,dc=example,dc=com','password')
conn.simple_bind_s('uid=gauss,dc=example,dc=com','password1')

