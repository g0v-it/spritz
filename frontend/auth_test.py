"""Authentication module for testing pourpose,
don't use in production.
If username and password in the "votinguser" table match
the login is successful.
"""
import os
import user

LOGIN_TEMPLATE = 'login_template.html'
CLIENT_ID = ''

ADD_UNKNOWN_USER=False

def get_auth_data(request):
    user_name = request.form['user_name']
    pass_word = request.form['pass_word']
    auth_data = {'username': user_name, 'password': pass_word}
    return auth_data

def auth(auth_data):
    u = user.load_user_by_username(auth_data['username'])
    if u.pass_word == auth_data['password']:
        return True
    return False


