#!/usr/bin/env python3
import unittest
import voter
import user 
import votation
from datetime import datetime
import random

class voter_test(unittest.TestCase):
        
    def test_insert(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        o.voted = 1
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.insert_dto(o)
        self.assertTrue(voter.has_voted(o))
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
    def test_insert2(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        o.voted = 0
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.insert_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
    def test_insert3(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        o.voted = 0
        voter.delete_dto(o)
        self.assertTrue( voter.insert_dto(o))
        self.assertFalse(voter.insert_dto(o))
        voter.delete_dto(o)
    def test_count_voters1(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        o.voted = 1
        voter.insert_dto(o)
        self.assertEqual(1, voter.count_voters(o.votation_id) )
        voter.delete_dto(o)
    def test_count_voters2(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        o.voted = 0
        voter.insert_dto(o)
        self.assertEqual(0, voter.count_voters(o.votation_id) )
        voter.delete_dto(o)
    def test_update_dto1(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        o.voted = 0
        voter.delete_dto(o)
        voter.insert_dto(o)
        self.assertFalse(voter.has_voted(o))
        o.voted = 1
        voter.update_dto(o) 
        self.assertTrue(voter.has_voted(o))
        voter.delete_dto(o)
    def test_insert_voters_array(self):
        votation_id = 1000
        u1 = "aldo"
        u2 = "beppe"
        u3 = "carlo"
        ar = [u1,u2,u3]

        u = user.load_user_by_username(u1)       
        o = voter.voter_dto()
        o.votation_id = votation_id
        o.user_id = u.user_id
        voter.delete_dto(o)

        u = user.load_user_by_username(u2)       
        o = voter.voter_dto()
        o.votation_id = votation_id
        o.user_id = u.user_id
        voter.delete_dto(o)

        u = user.load_user_by_username(u3)       
        o = voter.voter_dto()
        o.votation_id = votation_id
        o.user_id = u.user_id
        voter.delete_dto(o)

        self.assertEqual(3,voter.insert_voters_array(votation_id, ar) )
        u = user.load_user_by_username(u1)       
        o = voter.voter_dto()
        o.votation_id = votation_id
        o.user_id = u.user_id
        voter.delete_dto(o)
        self.assertEqual(1,voter.insert_voters_array(votation_id, ar) )
        self.assertEqual(0,voter.insert_voters_array(votation_id, ar) )
    def test_insert_unknown_voter(self):
        votation_id = 1000
        ar = ["nobody",]
        self.assertEqual(0,voter.insert_voters_array(votation_id,ar))
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
        v = votation.votation_dto()
        v.votation_description = 'Votation automated test for voter1'
        v.description_url = ""
        v.votation_type = votation.TYPE_SIMPLE_MAJORITY
        v.promoter_user.user_id = 1
        v.begin_date = datetime(2018,1,1)
        v.end_date = datetime(2018,1,15)
        v.votation_status = 1
        v.list_voters = 1
        self.assertTrue( votation.insert_votation_dto(v) )

        o = voter.voter_dto()
        o.votation_id = v.votation_id
        o.user_id = 2
        o.voted = 0
        voter.delete_dto(o)
        voter.insert_dto(o)
        self.assertTrue(voter.is_voter(o.votation_id,o.user_id))
        voter.delete_dto(o)

        votation.deltree_votation_by_id(v.votation_id)

    def test_is_voter_votation_null(self):
        o = voter.voter_dto()
        o.votation_id = 1000
        o.user_id = 1
        o.voted = 0
        voter.insert_dto(o)
        self.assertFalse(voter.is_voter(o.votation_id,o.user_id))

    def test_set_voted_no_list(self):
        # create a votation no list
        v = votation.votation_dto()
        v.votation_description = 'Votation automated test no list ' + str(random.randint(0,10000 ))
        v.description_url = ""
        v.votation_type = votation.TYPE_SIMPLE_MAJORITY
        v.promoter_user.user_id = 1
        v.begin_date = datetime(2018,1,1)
        v.end_date = datetime(2018,1,15)
        v.votation_status = 1
        v.list_voters = 0 # <<---- no list
        self.assertTrue( votation.insert_votation_dto(v) )

        # run set_voted
        o = voter.voter_dto()
        o.votation_id = v.votation_id
        o.user_id = 2
        # should perform insert
        self.assertTrue(voter.is_voter(o.votation_id, o.user_id))
        self.assertTrue(voter.set_voted(o))
        self.assertTrue(voter.has_voted(o))
        # should perform update
        self.assertTrue(voter.set_voted(o))
        self.assertTrue(voter.has_voted(o))
        self.assertTrue(voter.is_voter(o.votation_id, o.user_id))

        votation.deltree_votation_by_id(v.votation_id)

    def test_set_voted_with_list(self):
        # create a votation no list
        v = votation.votation_dto()
        v.votation_description = 'Votation automated test with list ' + str(random.randint(0,10000 ))
        v.description_url = ""
        v.votation_type = votation.TYPE_SIMPLE_MAJORITY
        v.promoter_user.user_id = 1
        v.begin_date = datetime(2018,1,1)
        v.end_date = datetime(2018,1,15)
        v.votation_status = 1
        v.list_voters = 1 # <<---- with list
        self.assertTrue( votation.insert_votation_dto(v) )

        # insert a voter 
        o = voter.voter_dto()
        o.votation_id = v.votation_id
        o.user_id = 2
        o.voted = 0
        self.assertFalse(voter.is_voter(o.votation_id, o.user_id))
        voter.insert_dto(o)
        self.assertTrue(voter.is_voter(o.votation_id, o.user_id))

        # run set_voted()
        self.assertFalse(voter.has_voted(o))
        self.assertTrue(voter.set_voted(o))
        self.assertTrue(voter.has_voted(o))

        votation.deltree_votation_by_id(v.votation_id)


if __name__ == '__main__':
    unittest.main()
