#!/usr/bin/env python3
import unittest
import voter

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

            
    


if __name__ == '__main__':
    unittest.main()
