#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
config.db = db

import unittest
import user_test
import votation_test
import option_test
#import guarantor_test
#import backend_test
import vote_test
import voter_test

#
# WARNING!
# This test suite don't work with SQLAlchemy
#

test_suite = unittest.TestSuite()
#test_suite.addTest(unittest.makeSuite(user_test.user_test))
# test_suite.addTest(unittest.makeSuite(votation_test.votation_test))
# test_suite.addTest(unittest.makeSuite(option_test.option_test))
test_suite.addTest(unittest.makeSuite(vote_test.vote_test_no_voters))
# test_suite.addTest(unittest.makeSuite(vote_test.vote_test_voters))
# test_suite.addTest(unittest.makeSuite(voter_test.voter_test))

r = unittest.TextTestRunner()
r.run(test_suite)
