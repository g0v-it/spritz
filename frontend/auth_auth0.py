from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv

import user
from flask_babel import gettext
_ = gettext
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import config

ADD_UNKNOWN_USER = True
LOGIN_TEMPLATE = 'login_auth0_template.html'
CLIENT_ID = env.get('CLIENT_ID')
CLIENT_SECRET = env.get('CLIENT_SECRET')
CALLBACK_URL = env.get('CALLBACK_URL')
API_BASE_URL = env.get('API_BASE_URL')
ACCESS_TOKEN_URL = env.get('ACCESS_TOKEN_URL')
AUTHORIZE_URL = env.get('AUTHORIZE_URL')
oauth = OAuth(config.app)

auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url=API_BASE_URL,
    access_token_url=ACCESS_TOKEN_URL,
    authorize_url=AUTHORIZE_URL,
    client_kwargs={
        'scope': 'openid profile email',
    },
)

ADD_UNKNOWN_USER=False

def get_auth_data():
    return auth0.authorize_redirect(redirect_uri=CALLBACK_URL)


def auth():
    message = _('Login failed')
    return_code = False

    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    if userinfo:
        return_code = True
        message = _('Login successful')
    else:
        message = _('Access not allowed.')
    auth_result = {'username': userinfo['email'], 'message': message, 'logged_in': return_code}
    return auth_result

