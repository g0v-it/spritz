#!/usr/bin/env python3
import unittest
import voter

class voter_test(unittest.TestCase):
        
    def test_insert(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
        voter.insert_dto(o)
        self.assertTrue(voter.has_voted(o))
        voter.delete_dto(o)
        self.assertFalse(voter.has_voted(o))
    def test_count_voters1(self):
        o = voter.voter_dto()
        o.user_id = 1000
        o.votation_id = 999
        voter.insert_dto(o)
        self.assertEqual(1, voter.count_voters(o.votation_id) )
        voter.delete_dto(o)
            
    


if __name__ == '__main__':
    unittest.main()
