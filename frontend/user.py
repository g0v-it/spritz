import config
from flask_login import UserMixin
from model import VotingUser

if config.AUTH == 'ldap':
    import auth_ldap as auth
if config.AUTH == 'google':
    import auth_google as auth
if config.AUTH == 'test':
    import auth_test as auth
    
db = config.db
        
class User(UserMixin):
    """This class is for the Flask-login session"""
    def __init__(self, user_name=''):
        self.user_name = user_name
        self.u = load_user_by_username(user_name)    
    def get_id(self):
        return str(self.user_name) # must be unicode
    def try_to_authenticate(self, pass_word):
        if self.u:
            return auth.auth(self.user_name, pass_word)
        return False
    def is_valid(self):
        return self.u != None


def load_user_by_id(user_id):
    """Returns a user_dto object or None"""
    u = db.session.query(VotingUser).filter(VotingUser.user_id == user_id).first()
    return u

def load_user_by_username(user_name):
    """Returns a user_dto object or None"""
    u = db.session.query(VotingUser).filter(VotingUser.user_name == user_name).first()
    if auth.ADD_UNKNOWN_USER:
        if u == None:
            u = VotingUser(user_name=user_name, pass_word='no password')
            db.session.add(u)
            db.session.commit()
    return u

def delete_user_by_id(user_id):
    result = False
    u = db.session.query(VotingUser).filter(VotingUser.user_id == user_id).first()
    if u:
        db.session.delete(u)
        db.session.commit()
        result = True
    return result

def delete_user_by_username(user_name):
    result = False
    u = db.session.query(VotingUser).filter(VotingUser.user_name == user_name).first()
    if u:
        db.session.delete(u)
        db.session.commit()
        result = True
    return result

