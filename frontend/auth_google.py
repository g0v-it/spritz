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

def auth(auth_data):
    return_code = False
    message = "ok"
    try:
        token = auth_data["credential"]
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        #userid = idinfo['sub']
        userid = idinfo['email']
        message = 'Valid token'
        return_code = True
    except ValueError:
        # Invalid token
        message = 'Invalid token'
        return_code = False
    auth_result = {'username': userid, 'message': message, 'logged_in': return_code}
    return auth_result


def logout_action():
    return render_template('logout_template.html', pagetitle="Logout")

