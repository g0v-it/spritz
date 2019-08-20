"""Authentication module for superauth
"""
import os
import urllib.request
import hashlib 
import json

ADD_UNKNOWN_USER = True
LOGIN_TEMPLATE = 'login_superauth_template.html'
CLIENT_ID='spritz_localhost'
CLIENT_SECRET='faec19ef7fcf49de960b8f44803d98dbb2dffd5e1e124ba9847947006b806209'
RETURN_URL = 'https://superauth.com/spritz_localhost'

def get_auth_data(request):
    token = request.args().get('token', None)
    state = request.args().get('state', None)
    return {'token': token, 'state': state}


def auth(auth_data):
    token = auth_data['token']
    state = auth_data['state']
    return_code = False
    message = "Login not successful"
    user_name = ''
    if state != 'abc123':
        message = "Login not successful, (wrong state)"
    else:
        m = hashlib.sha256()
        m.update(token.encode())
        m.update(CLIENT_ID.encode())
        m.update(CLIENT_SECRET.encode())
        token_value = m.hexdigest()
        getuserinfourl = 'https://superauth.com/v1/getuserinfo?token_type=check_token&token={}&client_id={}&token_value={}'.format(token,CLIENT_ID,token_value)
        contents = urllib.request.urlopen(getuserinfourl).read()
        j = json.loads(contents)
        if "user" in j.keys():
            user_name = j["user"]["email"]
            message = "Login successful"
            return_code = True
        else:
            message = "Login not successful, (no username)"
    return {'username': user_name, 'message': message, 'return_code': return_code}


