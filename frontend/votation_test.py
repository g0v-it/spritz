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
import votation_dao
import votation_bo
import option_dao
from model import Votation,Option
import random
from datetime import datetime
from config import MSG_INFO,MSG_OK,MSG_KO

class votation_test(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_insert(self):
        #print("VOTATION TEST")
        v = Votation( \
            votation_description = 'Votation automated test ' + str(random.randint(0,500)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_DRAW , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(v) )
        self.assertGreater(v.votation_id,0)
        v1 = votation_dao.load_votation_by_id(v.votation_id)
        self.assertIsNotNone(v1)
        self.assertIsNotNone(v1.promoter_user)
        self.assertEqual(v.votation_id, v1.votation_id)
        self.assertEqual(v.votation_description, v1.votation_description)
        self.assertEqual(v.votation_type, v1.votation_type)
        self.assertEqual(v.promoter_user.user_id, v1.promoter_user.user_id)
        self.assertEqual(v.begin_date, v1.begin_date)
        self.assertEqual(v.end_date, v1.end_date)
        votation_dao.delete_votation_by_id(v.votation_id)
        v1 = votation_dao.load_votation_by_id(v.votation_id)
        self.assertIsNone(v1)

    def test_validate_string_date(self):
        self.assertTrue(votation_dao.validate_string_date("2018-01-01"))
        self.assertTrue(votation_dao.validate_string_date("1999-01-01"))
        self.assertTrue(votation_dao.validate_string_date("2999-12-31"))
        self.assertFalse(votation_dao.validate_string_date(""))
        self.assertFalse(votation_dao.validate_string_date("a"))
        self.assertFalse(votation_dao.validate_string_date("2180"))
        self.assertFalse(votation_dao.validate_string_date("2018-32-10"))
        self.assertFalse(votation_dao.validate_string_date("2018-02-30"))

    def test_insert_duplicate_description(self):
        DESCRIPTION = "Duplicate description test"
        ar = votation_dao.load_votations()
        for old_votation in ar:
            if old_votation.votation_description == DESCRIPTION:
                votation_bo.deltree_votation_by_id(old_votation.votation_id)
        v = Votation( \
            votation_description = DESCRIPTION , \
            description_url = '' , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = votation_dao.STATUS_WAIT_FOR_CAND_AND_GUAR , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(v) )
        db.session.commit()
        v1 = Votation( \
            votation_description = DESCRIPTION , \
            description_url = 'ciao' , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 2 , \
            begin_date = datetime(2018,1,2) , \
            end_date = datetime(2018,1,16) , \
            votation_status = votation_dao.STATUS_WAIT_FOR_CAND_AND_GUAR , \
            list_voters = 0)
        self.assertFalse( votation_dao.insert_votation_dto(v1) )
        db.session.rollback()
        votation_dao.delete_votation_by_id(v.votation_id)
        db.session.commit()

    def test_update_end_date(self):
        v = Votation( \
            votation_description = 'Update end date test ' + str(random.randint(0,500)) , \
            description_url = '' , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,2,1) , \
            votation_status = votation_dao.STATUS_WAIT_FOR_CAND_AND_GUAR , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(v) )
        new_end_date = datetime(2019,12,31,8,34)
        votation_bo.update_end_date(v.votation_id, new_end_date)
        v2 = votation_dao.load_votation_by_id(v.votation_id)
        self.assertEqual(new_end_date, v2.end_date)
        votation_bo.deltree_votation_by_id(v.votation_id)
    
    def test_insert_votation_and_options_1(self):
        descr = 'Votation and options 1 automated test ' + str(random.randint(0,500))
        v = Votation( \
            votation_description = descr , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        txt_options = "option_test_A\noption_test_B\n option_test_C"
        result = votation_bo.insert_votation_with_options(v,txt_options)
        self.assertEqual(MSG_OK,result[1])
        ar = votation_dao.load_votations()
        check = False
        for w in ar:
            if w.votation_description == descr:
                check = True
                break
        self.assertTrue(check)
        opt_ar = option_dao.load_options_by_votation(w.votation_id)
        self.assertEqual(3,len(opt_ar))
        votation_bo.deltree_votation_by_id(w.votation_id)

    def test_insert_votation_and_options_2(self):
        """Begin an end dates are in the wrong order"""
        descr = 'Votation and options 2 automated test ' + str(random.randint(0,500))
        v = Votation( \
            votation_description = descr , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,2,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        txt_options = "option_test_A\noption_test_B\n option_test_C"
        result = votation_bo.insert_votation_with_options(v,txt_options)
        self.assertEqual(MSG_KO,result[1])
        ar = votation_dao.load_votations()
        check = False
        for w in ar:
            if w.votation_description == descr:
                check = True
        self.assertFalse(check)

    def test_insert_votation_and_options_3(self):
        """Duplicate description of votation"""
        descr = 'Votation and options duplicate description ' + str(random.randint(0,500))
        v = Votation( \
            votation_description = descr , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        votation_dao.insert_votation_dto(v)
        db.session.commit()
        v = Votation( \
            votation_description = descr , \
            description_url = "hello" , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 2 , \
            begin_date = datetime(2018,1,2) , \
            end_date = datetime(2018,1,28) , \
            votation_status = 1 , \
            list_voters = 1)
        txt_options = "option_test_X\noption_test_Y\n option_test_Z"
        result = votation_bo.insert_votation_with_options(v,txt_options)
        self.assertEqual(MSG_KO,result[1])
        ar = votation_dao.load_votations()
        check = False
        for w in ar:
            if w.votation_description == descr and w.promoter_user_id == 2:
                check = True
        self.assertFalse(check)


if __name__ == '__main__':
    unittest.main()
