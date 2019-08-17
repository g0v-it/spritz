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
import judgement_dao
import votation_dao
import votation_bo
from model import Option,Votation
from datetime import datetime

class jud_test(unittest.TestCase):
    __votation__ = None 

    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Votation for jud test ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_MAJORITY_JUDGMENT , \
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

    def test_text_ok(self):
        votation_id = self.__votation__.votation_id
        self.assertTrue(judgement_dao.save_judgements_from_text(votation_id,"""A
        X
        B"""))
        ar = judgement_dao.load_judgement_by_votation(votation_id)
        self.assertEqual(3, len(ar))
        self.assertEqual("B", ar[0].jud_name)
        self.assertEqual("X", ar[1].jud_name)
        self.assertEqual("A", ar[2].jud_name)
        self.assertEqual(0, ar[0].jud_value)
        self.assertEqual(1, ar[1].jud_value)
        self.assertEqual(2, ar[2].jud_value)

    def test_some_empty_lines(self):
        votation_id = self.__votation__.votation_id
        self.assertTrue(judgement_dao.save_judgements_from_text(votation_id,"""A

        X

        B"""))
        ar = judgement_dao.load_judgement_by_votation(votation_id)
        self.assertEqual(3, len(ar))
        self.assertEqual("B", ar[0].jud_name)
        self.assertEqual("X", ar[1].jud_name)
        self.assertEqual("A", ar[2].jud_name)
        self.assertEqual(0, ar[0].jud_value)
        self.assertEqual(1, ar[1].jud_value)
        self.assertEqual(2, ar[2].jud_value)

    def test_some_dup_lines(self):
        votation_id = self.__votation__.votation_id
        self.assertTrue(judgement_dao.save_judgements_from_text(votation_id,"""A
        X
        X
        B"""))
        ar = judgement_dao.load_judgement_by_votation(votation_id)
        self.assertEqual(4, len(ar))
        self.assertEqual("B", ar[0].jud_name)
        self.assertEqual("X", ar[1].jud_name)
        self.assertEqual("X", ar[2].jud_name)
        self.assertEqual("A", ar[3].jud_name)
        self.assertEqual(0, ar[0].jud_value)
        self.assertEqual(1, ar[1].jud_value)
        self.assertEqual(2, ar[2].jud_value)
        self.assertEqual(3, ar[3].jud_value)
            

if __name__ == '__main__':
    unittest.main()
