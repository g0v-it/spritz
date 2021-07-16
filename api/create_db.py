from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

if __name__ == '__main__':
    config.db = db
    import model
    db.create_all()
    
    u = model.VotingUser(user_name='aldo', pass_word='aldo')
    db.session.add(u)
    u = model.VotingUser(user_name='beppe', pass_word='beppe')
    db.session.add(u)
    u = model.VotingUser(user_name='carlo', pass_word='carlo')
    db.session.add(u)
    u = model.VotingUser(user_name='dario', pass_word='dario')
    db.session.add(u)
    u = model.VotingUser(user_name='ernesto', pass_word='ernesto')
    db.session.add(u)
    u = model.VotingUser(user_name='fabio', pass_word='fabio')
    db.session.add(u)

    db.session.commit()

