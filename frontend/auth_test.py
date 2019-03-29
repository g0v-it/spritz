"""Authentication module for testing pourpose
don't use in production
"""
import os
import user

LOGIN_TEMPLATE = 'login_template.html'
CLIENT_ID = ''

ADD_UNKNOWN_USER=False

def auth(user_name,token):
    u = user.load_user_by_username(user_name)
    if u.pass_word == token:
        return True
    return False


