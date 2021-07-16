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
import vote_dao
import vote_bo
import voter_dao
import option_dao
import votation_dao
from model import Votation,Vote,Option,Voter,Judgement
from datetime import datetime
import vote_maj_jud
import vote_simple
import votation_bo
import judgement_dao

class vote_test_no_voters(unittest.TestCase):
    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Votation for vote test ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(self.__votation__) )
        # set options
        o1 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option1')
        self.assertTrue(option_dao.insert_dto(o1))
        o2 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option2')
        self.assertTrue(option_dao.insert_dto(o2))
        o3 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option3')
        self.assertTrue(option_dao.insert_dto(o3))
        self.__option1 =  o1
        self.__option2 =  o2
        self.__option3 =  o3
        self.assertIsNotNone(o1.option_id)
        self.assertIsNotNone(o2.option_id)
        self.assertIsNotNone(o3.option_id)
        # set juds
        j1 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 0, jud_name = "bad")
        j2 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 1, jud_name = "medium")
        j3 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 2, jud_name = "good")
        judgement_dao.insert_dto(j1)
        judgement_dao.insert_dto(j2)
        judgement_dao.insert_dto(j3)
        db.session.commit()
        jud_array = judgement_dao.load_judgement_by_votation(self.__votation__.votation_id)
        self.__jud1 = jud_array[0]
        self.__jud2 = jud_array[1]
        self.__jud3 = jud_array[2]
        return super().setUp()

    def tearDown(self):
        votation_bo.deltree_votation_by_id(self.__votation__.votation_id)
        db.session.commit()
        return super().tearDown()

    def test_insert(self):
        u = Vote(vote_key = "vote_key123", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 5)
        self.assertTrue(vote_dao.insert_dto(u))
        ar = vote_dao.load_vote_by_key("vote_key123")
        self.assertEqual(1,len(ar))
        u1 = ar[0]
        self.assertIsNotNone(u1)
        self.assertEqual(u.votation_id, u1.votation_id)
        self.assertEqual(u.vote_key, u1.vote_key)
        self.assertEqual(u.option_id, u1.option_id)
        self.assertEqual(u.jud_value, u1.jud_value)
        vote_dao.delete_votes_by_key("vote_key123")
        ar = vote_dao.load_vote_by_key("vote_key123")
        self.assertEqual(0,len(ar))

    def test_median_calc3(self):
        self.assertEqual(1,vote_maj_jud.maj_jud_median_calc([1,1,1]))
        self.assertEqual(0,vote_maj_jud.maj_jud_median_calc([4,2,1]))
        self.assertEqual(1,vote_maj_jud.maj_jud_median_calc([5,10,0]))
        self.assertEqual(0,vote_maj_jud.maj_jud_median_calc([0,0,0]))
        self.assertEqual(2,vote_maj_jud.maj_jud_median_calc([10,0,20]))
        self.assertEqual(1,vote_maj_jud.maj_jud_median_calc([123,567,456]))
    def test_median_calc4(self):
        self.assertEqual(1,vote_maj_jud.maj_jud_median_calc([1,1,1,1]))
        self.assertEqual(0,vote_maj_jud.maj_jud_median_calc([7,2,1,1]))
        self.assertEqual(1,vote_maj_jud.maj_jud_median_calc([5,10,0,4]))
        self.assertEqual(0,vote_maj_jud.maj_jud_median_calc([0,0,0,0]))
        self.assertEqual(2,vote_maj_jud.maj_jud_median_calc([10,0,20,8]))
        self.assertEqual(1,vote_maj_jud.maj_jud_median_calc([123,567,456,34]))

    def test_compare(self):
        ar1 = [1,1,1]
        ar2 = [1,1,1]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  0)
        ar1 = [1,1,3]
        ar2 = [1,1,1]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  +1)
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar2,ar1),  -1)
        ar1 = [2,6,2] 
        ar2 = [3,4,3]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  +1)
        ar1 = [20,6,2] 
        ar2 = [3,4,30]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  -1)
        ar1 = [0,0,20] 
        ar2 = [0,10,0]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  +1)
        ar1 = [10,10,10] 
        ar2 = [10,11, 9]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  +1)
        ar1 = [5,10,5] 
        ar2 = [3,10, 7]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  -1)
        ar1 = [1000,1000,1000] 
        ar2 = [1000,1000,1000]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  0)
        ar1 = [1000,1000,1000] 
        ar2 = [950,960,1090]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  -1)
        ar1 = [0,0,1000] 
        ar2 = [0,0,900]
        self.assertEqual( vote_maj_jud.maj_jud_compare(ar1,ar2),  +1)
    def test_sort(self):
        r1 = vote_maj_jud.maj_jud_result(1,[100,100,100,100])
        r2 = vote_maj_jud.maj_jud_result(2,[50,100,150,100])
        r3 = vote_maj_jud.maj_jud_result(3,[100,150,100,50])
        r4 = vote_maj_jud.maj_jud_result(4,[50,100,100,150])
        a = sorted([r1,r2,r3,r4])
        b = a[::-1] # reverse the list
        self.assertEqual(4,b[0].option_id)
        self.assertEqual(2,b[1].option_id)
        self.assertEqual(1,b[2].option_id)
        self.assertEqual(3,b[3].option_id)
    def test_count_votes_by_option(self):
        votation_id = self.__votation__.votation_id
        option_id = self.__option1.option_id
        for i in range(10):
            u = Vote(votation_id = votation_id, option_id = option_id, \
                vote_key="vote_key1_" + str(i),jud_value=0)
            self.assertTrue(vote_dao.insert_dto(u))
        for i in range(20):
            u = Vote(votation_id = votation_id, option_id = option_id, \
                vote_key="vote_key2_" + str(i),jud_value=2)
            self.assertTrue(vote_dao.insert_dto(u))
        db.session.commit()
        self.assertEqual([10,0,20], vote_maj_jud.count_votes_by_option(votation_id,option_id))
    def test_mio(self):
        b = [22,19,19,15,19,14]
        r = [24,17,18,18,10,21]
        self.assertEqual( vote_maj_jud.maj_jud_compare(b,r), -1)
        b = [100,100,100,100,100,100]
        r = [100,100,100,100,100,100]
        self.assertEqual( vote_maj_jud.maj_jud_compare(b,r), 0)
        b = [100,100, 99,101,100,100]
        r = [100,100,100,100,100,100]
        self.assertEqual( vote_maj_jud.maj_jud_compare(b,r), +1)
        b = [100,100,100,100,100,100]
        r = [100,100,100,100, 99,101]
        self.assertEqual( vote_maj_jud.maj_jud_compare(b,r), -1)
    def test_save_simple(self):
        votation_id = self.__votation__.votation_id
        option_id = self.__option1.option_id
        self.assertTrue( vote_simple.save_vote(2,"akey",votation_id,option_id) )
        # check for duplicate key error:
        self.assertTrue( vote_simple.save_vote(2,"akey",votation_id,option_id) ) 
        self.assertFalse( vote_simple.save_vote(2,"anotherkey",votation_id,option_id) ) 
    def test_counting_votes1(self):
        votation_id = self.__votation__.votation_id
        n = vote_simple.counting_votes(votation_id)
        self.assertEqual({},n)
    def test_counting_votes2(self):
        votation_id = self.__votation__.votation_id
        v = Vote(vote_key = "vote_key1", \
            votation_id = votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(v))
        db.session.commit()
        n = vote_simple.counting_votes(votation_id)
        self.assertEqual({self.__option1.option_id:1,},n)
    def test_counting_votes3(self):
        votation_id = self.__votation__.votation_id
        v = Vote(vote_key = "vote_key1", \
            votation_id = votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(v))
        v = Vote(vote_key = "vote_key2", \
            votation_id = votation_id, \
            option_id = self.__option2.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(v))
        db.session.commit()
        d = vote_simple.counting_votes(votation_id)
        self.assertEqual(2,len(d.keys()))
    def test_counting_votes4(self):
        votation_id = self.__votation__.votation_id
        v = Vote(vote_key = "vote_key1", \
            votation_id = votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(v))
        v = Vote(vote_key = "vote_key2", \
            votation_id = votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(v))
        #db.session.flush()
        db.session.commit()
        d = vote_simple.counting_votes(votation_id)
        self.assertEqual(1,len(d.keys()))
    def test_counts_votes_by_votation_1(self):
        u = Vote(vote_key = "vote_key1", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 0)
        self.assertTrue(vote_dao.insert_dto(u))
        u = Vote(vote_key = "vote_key1", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option2.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(u))
        u = Vote(vote_key = "vote_key1", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option3.option_id, \
            jud_value = 2)
        self.assertTrue(vote_dao.insert_dto(u))
        db.session.commit()
        actual = vote_dao.counts_votes_by_votation(self.__votation__.votation_id)
        expected = {self.__option1.option_id: {0:1, 1:0, 2:0}, \
                    self.__option2.option_id: {0:0, 1:1, 2:0}, \
                    self.__option3.option_id: {0:0, 1:0, 2:1} }
        self.assertEqual(expected, actual)
    def test_counts_votes_by_votation_2(self):
        u = Vote(vote_key = "vote_key2", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 0)
        self.assertTrue(vote_dao.insert_dto(u))
        u = Vote(vote_key = "vote_key2", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option2.option_id, \
            jud_value = 1)
        self.assertTrue(vote_dao.insert_dto(u))
        u = Vote(vote_key = "vote_key2", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option3.option_id, \
            jud_value = 2)
        self.assertTrue(vote_dao.insert_dto(u))

        u = Vote(vote_key = "vote_key3", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option1.option_id, \
            jud_value = 0)
        self.assertTrue(vote_dao.insert_dto(u))
        u = Vote(vote_key = "vote_key3", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option2.option_id, \
            jud_value = 0)
        self.assertTrue(vote_dao.insert_dto(u))
        u = Vote(vote_key = "vote_key3", \
            votation_id = self.__votation__.votation_id, \
            option_id = self.__option3.option_id, \
            jud_value = 0)
        self.assertTrue(vote_dao.insert_dto(u))
        db.session.commit()
        actual = vote_dao.counts_votes_by_votation(self.__votation__.votation_id)
        expected = {self.__option1.option_id: {0:2, 1:0, 2:0}, \
                    self.__option2.option_id: {0:1, 1:1, 2:0}, \
                    self.__option3.option_id: {0:1, 1:0, 2:1} }
        self.assertEqual(expected, actual)

class vote_test_voters(unittest.TestCase):
    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Simple Votation with voters for vote test ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_SIMPLE_MAJORITY , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 1)
        self.assertTrue( votation_dao.insert_votation_dto(self.__votation__) )
        o1 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option1')
        self.assertTrue(option_dao.insert_dto(o1))
        o2 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option2')
        self.assertTrue(option_dao.insert_dto(o2))
        o3 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option3')
        self.assertTrue(option_dao.insert_dto(o3))
        self.__option1 =  o1
        self.__option2 =  o2
        self.__option3 =  o3
        self.assertIsNotNone(o1.option_id)
        self.assertIsNotNone(o2.option_id)
        self.assertIsNotNone(o3.option_id)
        # set juds
        j1 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 0, jud_name = "bad")
        j2 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 1, jud_name = "medium")
        j3 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 2, jud_name = "good")
        judgement_dao.insert_dto(j1)
        judgement_dao.insert_dto(j2)
        judgement_dao.insert_dto(j3)
        db.session.commit()
        jud_array = judgement_dao.load_judgement_by_votation(self.__votation__.votation_id)
        self.__jud1 = jud_array[0]
        self.__jud2 = jud_array[1]
        self.__jud3 = jud_array[2]
        voter1 = Voter(user_id = 1, votation_id = self.__votation__.votation_id, voted = 0)
        voter_dao.insert_dto(voter1)
        db.session.commit()
        return super().setUp()

    def tearDown(self):
        votation_bo.deltree_votation_by_id(self.__votation__.votation_id)
        db.session.commit()
        return super().tearDown()

    def test_save_simple_ok(self):
        votation_id = self.__votation__.votation_id
        option_id = self.__option1.option_id
        #def save_vote(user_id, vote_key,votation_id,option_id):
        self.assertTrue( vote_simple.save_vote(1,"akey123",votation_id,option_id) )
        ar = vote_dao.load_vote_by_key("akey123")
        for v in ar:
            if v.option_id == option_id:
                self.assertEqual(1, v.jud_value)
            else:
                self.assertEqual(0, v.jud_value)
        


class vote_test_new_save_DAO(unittest.TestCase):
    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Votation for vote test new save ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_MAJORITY_JUDGMENT , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(self.__votation__) )
        # set options
        o1 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option1')
        self.assertTrue(option_dao.insert_dto(o1))
        o2 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option2')
        self.assertTrue(option_dao.insert_dto(o2))
        o3 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option3')
        self.assertTrue(option_dao.insert_dto(o3))
        self.__option1 =  o1
        self.__option2 =  o2
        self.__option3 =  o3
        self.assertIsNotNone(o1.option_id)
        self.assertIsNotNone(o2.option_id)
        self.assertIsNotNone(o3.option_id)
        # set juds
        j1 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 0, jud_name = "bad")
        j2 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 1, jud_name = "medium")
        j3 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 2, jud_name = "good")
        judgement_dao.insert_dto(j1)
        judgement_dao.insert_dto(j2)
        judgement_dao.insert_dto(j3)
        db.session.commit()
        jud_array = judgement_dao.load_judgement_by_votation(self.__votation__.votation_id)
        self.__jud1 = jud_array[0]
        self.__jud2 = jud_array[1]
        self.__jud3 = jud_array[2]
        return super().setUp()

    def tearDown(self):
        votation_bo.deltree_votation_by_id(self.__votation__.votation_id)
        db.session.commit()
        return super().tearDown()

    def test_save_ok(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertTrue( vote_dao.save_vote(self.__votation__.votation_id, vote_key, [0,1,2]) )
        ar = vote_dao.load_vote_by_key(vote_key)
        self.assertEqual(3,len(ar))
        check = True
        for v in ar:
            if (v.option_id == self.__option1.option_id and \
                v.jud_value == 0) or \
               (v.option_id == self.__option2.option_id and \
               v.jud_value == 1) or \
               (v.option_id == self.__option3.option_id and \
               v.jud_value == 2): 
                check = True
            else:
                check = False
        self.assertTrue(check)
    def test_save_ok2(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertTrue( vote_dao.save_vote(self.__votation__.votation_id, vote_key, [1,2,2]) )
        ar = vote_dao.load_vote_by_key(vote_key)
        self.assertEqual(3,len(ar))
        check = True
        for v in ar:
            if (v.option_id == self.__option1.option_id and \
                v.jud_value == 1) or \
               (v.option_id == self.__option2.option_id and \
               v.jud_value == 2) or \
               (v.option_id == self.__option3.option_id and \
               v.jud_value == 2): 
                check = True
            else:
                check = False
        self.assertTrue(check)
    def test_save_wrong_array(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertFalse( vote_dao.save_vote(self.__votation__.votation_id, vote_key, [1,2]) )
        self.assertFalse( vote_dao.save_vote(self.__votation__.votation_id, vote_key, [1,2,3,4]) )
    def test_save_wrong_jud(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertFalse( vote_dao.save_vote(self.__votation__.votation_id, vote_key, [1,2,100]) )
    def test_save_null(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertFalse( vote_dao.save_vote(self.__votation__.votation_id, vote_key, [1,2,None]) )
    def test_save_wrong_votation_id(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertFalse( vote_dao.save_vote(333333, vote_key, [3,2,1]) )

class vote_test_new_save_BO(unittest.TestCase):
    def setUp(self):
        self.__votation__ = Votation( \
            votation_description = 'Votation for vote test new save ' + str(random.randint(0,50000)) , \
            description_url = "" , \
            votation_type = votation_dao.TYPE_MAJORITY_JUDGMENT , \
            promoter_user_id = 1 , \
            begin_date = datetime(2018,1,1) , \
            end_date = datetime(2018,1,15) , \
            votation_status = 2 , \
            list_voters = 0)
        self.assertTrue( votation_dao.insert_votation_dto(self.__votation__) )
        # set options
        o1 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option1')
        self.assertTrue(option_dao.insert_dto(o1))
        o2 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option2')
        self.assertTrue(option_dao.insert_dto(o2))
        o3 = Option(votation_id=self.__votation__.votation_id, \
             option_name = 'test.option3')
        self.assertTrue(option_dao.insert_dto(o3))
        self.__option1 =  o1
        self.__option2 =  o2
        self.__option3 =  o3
        self.assertIsNotNone(o1.option_id)
        self.assertIsNotNone(o2.option_id)
        self.assertIsNotNone(o3.option_id)
        # set juds
        j1 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 0, jud_name = "bad")
        j2 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 1, jud_name = "medium")
        j3 = Judgement(votation_id = self.__votation__.votation_id, \
            jud_value = 2, jud_name = "good")
        judgement_dao.insert_dto(j1)
        judgement_dao.insert_dto(j2)
        judgement_dao.insert_dto(j3)
        db.session.commit()
        jud_array = judgement_dao.load_judgement_by_votation(self.__votation__.votation_id)
        self.__jud1 = jud_array[0]
        self.__jud2 = jud_array[1]
        self.__jud3 = jud_array[2]
        return super().setUp()

    def tearDown(self):
        votation_bo.deltree_votation_by_id(self.__votation__.votation_id)
        db.session.commit()
        return super().tearDown()

    def test_save_ok(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertTrue( vote_bo.save_votes(user_id = 1, \
                                            vote_key=vote_key, \
                                            votation_id=self.__votation__.votation_id, \
                                            vote_array=[0,1,2]) )
        ar = vote_dao.load_vote_by_key(vote_key)
        self.assertEqual(3, len(ar) )
        self.assertTrue(voter_dao.has_voted(1,self.__votation__.votation_id))

    def test_save_twice(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        # first vote
        self.assertTrue( vote_bo.save_votes(user_id = 1, \
                                            vote_key=vote_key, \
                                            votation_id=self.__votation__.votation_id, \
                                            vote_array=[1,1,1]) )
        ar = vote_dao.load_vote_by_key(vote_key)
        self.assertEqual(3, len(ar) )
        self.assertTrue(voter_dao.has_voted(1,self.__votation__.votation_id))
        # second vote
        self.assertTrue( vote_bo.save_votes(user_id = 1, \
                            vote_key=vote_key, \
                            votation_id=self.__votation__.votation_id, \
                            vote_array=[2,2,2]) )

    def test_save_wrong_key(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        # first vote
        self.assertTrue( vote_bo.save_votes(user_id = 1, \
                                            vote_key=vote_key, \
                                            votation_id=self.__votation__.votation_id, \
                                            vote_array=[1,1,1]) )
        ar = vote_dao.load_vote_by_key(vote_key)
        self.assertEqual(3, len(ar) )
        self.assertTrue(voter_dao.has_voted(1,self.__votation__.votation_id))
        # second vote
        self.assertFalse( vote_bo.save_votes(user_id = 1, \
                            vote_key="WRONG KEY", \
                            votation_id=self.__votation__.votation_id, \
                            vote_array=[1,3,1]) )

    def test_save_wrong_array(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertFalse( vote_bo.save_votes(user_id = 1, \
                                            vote_key=vote_key, \
                                            votation_id=self.__votation__.votation_id, \
                                            vote_array=[1,2]) )
        self.assertFalse( vote_bo.save_votes(user_id = 1, \
                                            vote_key=vote_key, \
                                            votation_id=self.__votation__.votation_id, \
                                            vote_array=[1,2,3,4]) )

    def test_save_wrong_user(self):
        vote_key = 'vote_key' + str(random.randint(0,50000)) 
        self.assertFalse( vote_bo.save_votes(user_id = 999, \
                                            vote_key=vote_key, \
                                            votation_id=self.__votation__.votation_id, \
                                            vote_array=[1,2,2]) )


if __name__ == '__main__':
    unittest.main()

