#!/usr/bin/env python3
import unittest
import candidate
import user
import votation_dao
import random

class candidate_test(unittest.TestCase):
    def test_validate_1(self):
        o = candidate.candidate_dto()
        o.votation_id = 1
        self.assertEqual(1,candidate.validate_dto(o))
    def test_validate_2(self):
        o = candidate.candidate_dto()
        o.votation_id = None
        o.u.user_id = 1
        self.assertEqual(2,candidate.validate_dto(o))
    def test_validate_3(self):
        o = candidate.candidate_dto()
        o.votation_id = 1
        o.u.user_id = 999
        self.assertEqual(3,candidate.validate_dto(o))
    def test_validate_4(self):
        o = candidate.candidate_dto()
        o.votation_id = 1
        o.u.user_id = 1
        o.passphrase_ok = 0
        candidate.delete_dto(o)
        self.assertEqual(0,candidate.validate_dto(o))
    def test_validate_5(self):
        o = candidate.candidate_dto()
        o.votation_id = 999 # don't exist
        o.u.user_id = 1
        self.assertEqual(4,candidate.validate_dto(o))
    def test_insert_1(self):
        v = votation_dao.votation_dto()
        v.votation_description = 'Cand automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 1
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation_dao.insert_votation_dto(v)
        o = candidate.candidate_dto()
        o.votation_id = v.votation_id
        o.u.user_id = 1
    def test_load_1(self):
        v = votation_dao.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 1
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation_dao.insert_votation_dto(v)

        o1 = candidate.candidate_dto()
        o1.votation_id = v.votation_id
        o1.u.user_id = 1
        o2 = candidate.candidate_dto()
        o2.votation_id = v.votation_id
        o2.u.user_id = 2

        self.assertEqual(0,candidate.validate_dto(o1))
        self.assertEqual(0,candidate.validate_dto(o2))
        candidate.insert_dto(o1)
        candidate.insert_dto(o2)

        ar = candidate.load_candidate_by_votation(v.votation_id)
        self.assertEqual(2,len(ar))
        self.assertEqual(1,ar[0].order_n)
        self.assertEqual(2,ar[1].order_n)

    def test_load_2(self):
        v = votation_dao.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 1
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation_dao.insert_votation_dto(v)

        o1 = candidate.candidate_dto()
        o1.votation_id = v.votation_id
        o1.u.user_id = 1
        self.assertEqual(0,candidate.validate_dto(o1))
        candidate.insert_dto(o1)

        c = candidate.load_candidate(o1.votation_id, o1.u.user_id)
        self.assertEqual(o1.votation_id, c.votation_id)
        self.assertEqual(o1.u.user_id, c.u.user_id)
        self.assertEqual(1, c.order_n)
        self.assertEqual(0, c.passphrase_ok)

if __name__ == '__main__':
    unittest.main()
