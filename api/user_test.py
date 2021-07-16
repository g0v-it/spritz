#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
config.db = db

import unittest
import user
from model import VotingUser
import auth_test as auth

class user_test(unittest.TestCase):
    def setUp(self):
        auth.ADD_UNKNOWN_USER = False

    def test_delete_by_username(self):
        u = VotingUser(user_name='test.delete.name1',pass_word = 'secret')
        user.delete_user_by_username( u.user_name)
        db.session.add(u)
        self.assertTrue(user.delete_user_by_username( u.user_name))
        auth.ADD_UNKNOWN_USER = False
        u1 = user.load_user_by_username(u.user_name)
        self.assertIsNone( u1 )
        
    def test_delete_by_id(self):
        u = VotingUser(user_name='test.delete.id', pass_word='secret')
        user.delete_user_by_username( u.user_name)
        db.session.add(u)
        u1 = user.load_user_by_username(u.user_name)
        self.assertTrue(user.delete_user_by_id( u1.user_id) )
        self.assertIsNone( user.load_user_by_id(u1.user_id) )
        
    def test_load_by_username(self):
        u = VotingUser(user_name='test.user', pass_word='secret')
        user.delete_user_by_username(u.user_name)
        db.session.add(u)
        u1 = user.load_user_by_username(u.user_name)
        self.assertIsNotNone(u1)
        self.assertEqual(u.user_id, u1.user_id)
        self.assertEqual(u.user_name, u1.user_name)
        self.assertEqual(u.pass_word, u1.pass_word)
        user.delete_user_by_id(u.user_id)

    def test_load_by_id(self):
        self.assertIsNone(user.load_user_by_id(999))
        

if __name__ == '__main__':
    unittest.main()
