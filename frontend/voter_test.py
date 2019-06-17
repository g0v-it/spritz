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
import voter
import votation
import user
from model import Votation,Voter
from datetime import datetime

class voter_test(unittest.TestCase):
    __votation__ = None 
    __votation_list__ = None

    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Votation for voter test ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation.insert_votation_dto(self.__votation__) )
        self.__votation_list__ = Votation( \
            votation_description = 'Votation for voter test (list) ' + str(random.randint(0,500)) , \
            description_url = "" , \
            votation_type = votation.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 1)
        self.assertTrue( votation.insert_votation_dto(self.__votation_list__) )
        db.session.commit()
        return super().setUp()

    def tearDown(self):
        votation.deltree_votation_by_id(self.__votation__.votation_id)
        votation.deltree_votation_by_id(self.__votation_list__.votation_id)
        db.session.commit()
        return super().tearDown()
        
    def test_insert(self):
        o = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=1)
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.insert_dto(o)
        self.assertTrue(voter.has_voted(o))
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
    def test_insert2(self):
        o = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=0)
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.insert_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
    def test_insert3(self):
        o1 = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=0)
        o2 = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=0)
        voter.delete_dto(o1)
        self.assertTrue( voter.insert_dto(o1))
        #self.assertFalse(voter.insert_dto(o2)) this don't thrown errors in sqlalchemy
        voter.delete_dto(o1)
    def test_count_voters1(self):
        o = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=1)
        voter.insert_dto(o)
        self.assertEqual(1, voter.count_voters(o.votation_id) )
        voter.delete_dto(o)
    def test_count_voters2(self):
        o = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=0)
        voter.insert_dto(o)
        self.assertEqual(0, voter.count_voters(o.votation_id) )
        voter.delete_dto(o)
    def test_update_dto1(self):
        o = Voter(user_id=1, votation_id=self.__votation__.votation_id, voted=0)
        voter.delete_dto(o)
        voter.insert_dto(o)
        self.assertFalse(voter.has_voted(o))
        o.voted = 1
        voter.update_dto(o) 
        self.assertTrue(voter.has_voted(o))
        voter.delete_dto(o)
    def test_insert_voters_array_3(self):
        votation_id = self.__votation__.votation_id
        u1 = "aldo"
        u2 = "beppe"
        u3 = "carlo"
        ar = [u1,u2,u3]
        self.assertEqual(3,voter.insert_voters_array(votation_id, ar) )
        db.session.commit()

    def test_insert_voters_array_1(self):
        votation_id = self.__votation__.votation_id
        u1 = "aldo"
        u2 = "beppe"
        u3 = "carlo"
        ar = [u1,u2]
        self.assertEqual(2,voter.insert_voters_array(votation_id, ar) )
        db.session.commit()
        ar = [u1,u2,u3]
        self.assertEqual(1,voter.insert_voters_array(votation_id, ar) )
        db.session.commit()

    def test_insert_voters_array_0(self):
        votation_id = self.__votation__.votation_id
        u1 = "aldo"
        u2 = "beppe"
        u3 = "carlo"
        ar = [u1,u2,u3]
        self.assertEqual(3,voter.insert_voters_array(votation_id, ar) )
        db.session.commit()
        self.assertEqual(0,voter.insert_voters_array(votation_id, ar) )
        db.session.commit()

    def test_insert_unknown_voter(self):
        votation_id = self.__votation__.votation_id
        ar = ["nobody",]
        self.assertEqual(0,voter.insert_voters_array(votation_id,ar))
        db.session.commit()

    def test_split1(self):
        expected = ["a","b","c"]
        actual = voter.split_string_remove_dup("""a
        b
        c""")
        self.assertEqual(set(expected), set(actual)  )
    def test_split2(self):
        expected = []
        actual = voter.split_string_remove_dup("")
        self.assertEqual(set(expected), set(actual)  )
    def test_split3(self):
        expected = ["a","b","c"]
        actual = voter.split_string_remove_dup("""a
        
        b 
        c""")
        self.assertEqual(set(expected), set(actual)  )
    def test_split4(self):
        expected = ["a","b","c"]
        actual = voter.split_string_remove_dup("""a
        b
        c 
        b""")
        self.assertEqual(set(expected), set(actual)  )
    def test_split5(self):
        expected = []
        actual = voter.split_string_remove_dup("")
        self.assertEqual(set(expected), set(actual)  )
    def test_split6(self):
        expected = []
        actual = voter.split_string_remove_dup("""
          
             
             """)
        self.assertEqual(set(expected), set(actual)  )

    def test_is_voter(self):
        o = Voter(user_id=2, votation_id=self.__votation__.votation_id, voted=0)
        voter.delete_dto(o)
        voter.insert_dto(o)
        self.assertTrue(voter.is_voter(o.votation_id,o.user_id))
        voter.delete_dto(o)


    def test_set_voted_no_list(self):
        # run set_voted
        o = Voter(user_id=2, votation_id=self.__votation__.votation_id, voted=0)
        # should perform insert
        self.assertTrue(voter.is_voter(o.votation_id, o.user_id))
        self.assertTrue(voter.set_voted(o))
        self.assertTrue(voter.has_voted(o))
        # should perform update
        self.assertTrue(voter.set_voted(o))
        self.assertTrue(voter.has_voted(o))
        self.assertTrue(voter.is_voter(o.votation_id, o.user_id))


    def test_set_voted_with_list(self):
        # insert a voter 
        o = Voter(user_id=2, votation_id=self.__votation_list__.votation_id, voted=0)
        self.assertFalse(voter.is_voter(o.votation_id, o.user_id))
        voter.insert_dto(o)
        self.assertTrue(voter.is_voter(o.votation_id, o.user_id))

        # run set_voted()
        self.assertFalse(voter.has_voted(o))
        self.assertTrue(voter.set_voted(o))
        self.assertTrue(voter.has_voted(o))

if __name__ == '__main__':
    unittest.main()
