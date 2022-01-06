"""Authentication module for testing pourpose,
don't use in production.
If username and password in the "votinguser" table match
the login is successful.
"""
import os
import user
from flask_babel import gettext
from flask import redirect,url_for,render_template

_ = gettext

LOGIN_TEMPLATE = 'login_template.html'
CLIENT_ID = ''

ADD_UNKNOWN_USER=False

def get_auth_data(request):
    user_name = request.form['user_name']
    pass_word = request.form['pass_word']
    auth_data = {'username': user_name, 'password': pass_word}
    return auth_data

def auth(auth_data):
    message = _('Login failed')
    return_code = False
    user_name = auth_data['username']
    u = user.load_user_by_username(user_name)
    if u and u.pass_word == auth_data['password']:
        return_code = True
        message = _('Login successful')
    else:
        message = _('Wrong user or password')
    auth_result = {'username': user_name, 'message': message, 'logged_in': return_code}
    return auth_result

def logout_action():
    return render_template('logout_template.html', pagetitle="Logout")
