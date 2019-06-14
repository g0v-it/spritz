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
import votation
from model import Votation,Option
import random
from datetime import datetime

class votation_test(unittest.TestCase):
        
    def test_insert(self):
        v = Votation( \
            votation_description = 'Votation automated test ' + str(random.randint(0,500)) , \
            description_url = "" , \
            votation_type = votation.TYPE_DRAW , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation.insert_votation_dto(v) )
        self.assertGreater(v.votation_id,0)
        v1 = votation.load_votation_by_id(v.votation_id)
        self.assertIsNotNone(v1)
        self.assertEqual(v.votation_id, v1.votation_id)
        self.assertEqual(v.votation_description, v1.votation_description)
        self.assertEqual(v.votation_type, v1.votation_type)
        self.assertEqual(v.promoter_user.user_id, v1.promoter_user.user_id)
        self.assertEqual(v.begin_date, v1.begin_date)
        self.assertEqual(v.end_date, v1.end_date)
        votation.delete_votation_by_id(v.votation_id)
        v1 = votation.load_votation_by_id(v.votation_id)
        self.assertIsNone(v1)

    def test_validate_string_date(self):
        self.assertTrue(votation.validate_string_date("2018-01-01"))
        self.assertTrue(votation.validate_string_date("1999-01-01"))
        self.assertTrue(votation.validate_string_date("2999-12-31"))
        self.assertFalse(votation.validate_string_date(""))
        self.assertFalse(votation.validate_string_date("a"))
        self.assertFalse(votation.validate_string_date("2180"))
        self.assertFalse(votation.validate_string_date("2018-32-10"))
        self.assertFalse(votation.validate_string_date("2018-02-30"))

    def test_insert_duplicate_description(self):
        v = Votation( \
            votation_description = 'Duplicate description test' , \
            description_url = '' , \
            votation_type = votation.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = votation.STATUS_WAIT_FOR_CAND_AND_GUAR , \
            list_voters = 0)
        self.assertTrue( votation.insert_votation_dto(v) )
        v1 = Votation( \
            votation_description = 'Duplicate description test' , \
            description_url = '' , \
            votation_type = votation.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 2 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = votation.STATUS_WAIT_FOR_CAND_AND_GUAR , \
            list_voters = 0)
        self.assertFalse( votation.insert_votation_dto(v1) )
        votation.delete_votation_by_id(v.votation_id)

    def test_update_end_date(self):
        v = Votation( \
            votation_description = 'Update end date test ' + str(random.randint(0,500)) , \
            description_url = '' , \
            votation_type = votation.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,2,1) , \
            votation_status = votation.STATUS_WAIT_FOR_CAND_AND_GUAR , \
            list_voters = 0)
        self.assertTrue( votation.insert_votation_dto(v) )
        new_end_date = datetime(2019,12,31,8,34)
        votation.update_end_date(v.votation_id, new_end_date)
        
        v2 = votation.load_votation_by_id(v.votation_id)
        self.assertEqual(new_end_date, v2.end_date)

        votation.delete_votation_by_id(v.votation_id)
    
    def test_insert_votation_and_options(self):
        v = Votation( \
            votation_description = 'Votation and options automated test ' + str(random.randint(0,500)) , \
            description_url = "" , \
            votation_type = votation.TYPE_DRAW , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation.insert_votation_dto(v) )        
        o1 = Option(votation_id=v.votation_id,option_name = "option 1",description="")
        o2 = Option(votation_id=v.votation_id,option_name = "option 2",description="")
        o3 = Option(votation_id=v.votation_id,option_name = "option 3",description="")
        ar = [o1,o2,o3]
        self.assertTrue(votation.insert_votation_and_options(v,ar))

if __name__ == '__main__':
    unittest.main()
