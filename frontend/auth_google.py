"""Authentication module for google sign in
"""
import os
from google.oauth2 import id_token
from google.auth.transport import requests

ADD_UNKNOWN_USER = True
LOGIN_TEMPLATE = 'login_google_template.html'
CLIENT_ID='1005534143144-rumegcgece72qbjq30ganftaf3vhv2p2.apps.googleusercontent.com'

def get_auth_data(request):
    user_name = request.form['user_name']
    pass_word = request.form['pass_word']
    auth_data = {'username': user_name, 'password': pass_word}
    return auth_data


def auth(auth_data):
    try:
        user_name = auth_data['username']
        token = auth_data['password']
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            #raise ValueError('Wrong issuer.')
            return False

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        user_name = idinfo['email']
        return True
    except ValueError:
        # Invalid token
        pass
    return False


