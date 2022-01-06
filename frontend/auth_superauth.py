"""Authentication module for superauth
"""
import os
import user
import urllib.request
import hashlib 
import json
from flask_babel import gettext
from flask import redirect,url_for,render_template
_ = gettext

ADD_UNKNOWN_USER = True
LOGIN_TEMPLATE = 'login_superauth_template.html'
CLIENT_ID=os.environ.get('SUPERAUTH_LOGIN_CLIENT_ID')
CLIENT_SECRET=os.environ.get('SUPERAUTH_LOGIN_CLIENT_SECRET')


def get_auth_data(request):
    token = request.args.get('token', None)
    state = request.args.get('state', None)
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
            message = _("Login successful")
            u = user.load_user_by_username(user_name)
            return_code = True
        else:
            message = _("Login not successful, (no username)")
    return {'username': user_name, 'message': message, 'logged_in': return_code}


def logout_action():
    return render_template('logout_template.html', pagetitle="Logout")
