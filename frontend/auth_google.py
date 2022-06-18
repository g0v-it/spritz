"""Authentication module for google sign in
"""
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from flask_babel import gettext
from flask import redirect,url_for,render_template

import user
_ = gettext

ADD_UNKNOWN_USER = True
LOGIN_TEMPLATE = 'login_google_template.html'
CLIENT_ID = os.environ.get('GOOGLE_LOGIN_CLIENT_ID')

def get_auth_data(request):
    user_name = request.form['user_name']
    pass_word = request.form['pass_word']
    auth_data = {'username': user_name, 'password': pass_word}
    return auth_data


def auth(auth_data):
    return_code = False
    user_name = auth_data['user_name']
    message = _('Login failed')
    token = auth_data['pass_word']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            #raise ValueError('Wrong issuer.')
            return_code = False
            message = _('Login failed')
        else:
            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            user_name = idinfo['email']
            user.load_user_by_username(user_name)
            return_code =  True
            message = _('Login successful')
    except ValueError:
        # Invalid token
        message = 'Invalid token'
        return_code = False
    auth_result = {'username': user_name, 'message': message, 'logged_in': return_code}
    return auth_result


def logout_action():
    return render_template('logout_template.html', pagetitle="Logout")

