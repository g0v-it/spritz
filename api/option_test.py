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
import option_dao
import votation_dao
import votation_bo
from model import Option,Votation
from datetime import datetime

class option_test(unittest.TestCase):
    __votation__ = None 

    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Votation for option test ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_DRAW , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(self.__votation__) )
        db.session.commit()
        return super().setUp()

    def tearDown(self):
        votation_bo.deltree_votation_by_id(self.__votation__.votation_id)
        db.session.commit()
        return super().tearDown()

    def test_insert(self):
        votation_id = self.__votation__.votation_id
        u = Option(votation_id=votation_id,option_name = 'test.option')
        self.assertTrue( option_dao.insert_dto(u))
        self.assertGreater(u.option_id, 0)
        ar = option_dao.load_options_by_votation(votation_id)
        self.assertEqual(1,len(ar))
        u1 = ar[0]
        self.assertIsNotNone(u1)
        self.assertEqual(u.votation_id, u1.votation_id)
        self.assertEqual(u.option_name, u1.option_name)
        self.assertTrue(option_dao.delete_dto(u1))
        ar = option_dao.load_options_by_votation(votation_id)
        self.assertEqual(0,len(ar))

    def test_text_ok(self):
        votation_id = self.__votation__.votation_id
        option_dao.delete_options_by_votation(votation_id)
        self.assertTrue(option_dao.save_options_from_text(votation_id,"""test row 1
        test row 2
        test row 3""") )
        ar = option_dao.load_options_by_votation(votation_id)
        self.assertEqual(3, len(ar))
        self.assertEqual("TEST ROW 1", ar[0].option_name)
        self.assertEqual("TEST ROW 2", ar[1].option_name)
        self.assertEqual("TEST ROW 3", ar[2].option_name)
        option_dao.delete_options_by_votation(votation_id)

    def test_text_empty(self):
        votation_id = self.__votation__.votation_id
        option_dao.delete_options_by_votation(votation_id)
        self.assertTrue( option_dao.save_options_from_text(votation_id,"""test row 1

        test row 2

        test row 3
        
        """) )
        ar = option_dao.load_options_by_votation(votation_id)
        self.assertEqual(3, len(ar))
        self.assertEqual("TEST ROW 1", ar[0].option_name)
        self.assertEqual("TEST ROW 2", ar[1].option_name)
        self.assertEqual("TEST ROW 3", ar[2].option_name)
        option_dao.delete_options_by_votation(votation_id)

    def test_text_duplicates(self):
        votation_id = self.__votation__.votation_id
        option_dao.delete_options_by_votation(votation_id)
        self.assertTrue( option_dao.save_options_from_text(votation_id,"""test row 3
        test row 2
        test row 3
        test row 1
        """) )
        ar = option_dao.load_options_by_votation(votation_id)
        self.assertEqual(3, len(ar))
        self.assertEqual("TEST ROW 1", ar[0].option_name)
        self.assertEqual("TEST ROW 2", ar[1].option_name)
        self.assertEqual("TEST ROW 3", ar[2].option_name)
        option_dao.delete_options_by_votation(votation_id)

if __name__ == '__main__':
    unittest.main()
