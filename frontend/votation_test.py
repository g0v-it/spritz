#!/usr/bin/env python3
import unittest
import votation
import random
from datetime import datetime

class votation_test(unittest.TestCase):
        
    def test_insert(self):
        v = votation.votation_dto()
        v.votation_description = 'Votation automated test ' + str(random.randint(0,500))
        v.description_url = ""
        v.votation_type = votation.TYPE_DRAW
        v.promoter_user.user_id = 1
        v.begin_date = datetime(2018,1,1)
        v.end_date = datetime(2018,1,15)
        v.votation_status = 2
        v.list_voters = 0
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
        v = votation.votation_dto()
        v.votation_description = 'Duplicate description test'
        v.description_url = ''
        v.votation_type = votation.TYPE_SIMPLE_MAJORITY
        v.promoter_user.user_id = 1
        v.begin_date = datetime(2018,1,1)
        v.end_date = datetime(2018,1,15)
        v.votation_status = votation.STATUS_WAIT_FOR_CAND_AND_GUAR
        v.list_voters = 0;
        self.assertTrue( votation.insert_votation_dto(v) )
        self.assertFalse( votation.insert_votation_dto(v) )
        votation.delete_votation_by_id(v.votation_id)
        

if __name__ == '__main__':
    unittest.main()
