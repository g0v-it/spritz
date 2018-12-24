#!/usr/bin/env python3
import unittest
import guarantor
import user
import votation
import random

class guarantor_test(unittest.TestCase):
    def test_validate_1(self):
        o = guarantor.guarantor_dto()
        o.votation_id = 1
        self.assertEqual(1,guarantor.validate_dto(o))
    def test_validate_2(self):
        o = guarantor.guarantor_dto()
        o.votation_id = None
        o.u.user_id = 1
        self.assertEqual(2,guarantor.validate_dto(o))
    def test_validate_3(self):
        o = guarantor.guarantor_dto()
        o.votation_id = 1
        o.u.user_id = 999
        self.assertEqual(3,guarantor.validate_dto(o))
    def test_validate_4(self):
        o = guarantor.guarantor_dto()
        o.votation_id = 1
        o.u.user_id = 1
        o.passphrase_ok = 0
        o.hash_ok = 0
        self.assertEqual(0,guarantor.validate_dto(o))
    def test_validate_5(self):
        o = guarantor.guarantor_dto()
        o.votation_id = 999 # don't exist
        o.u.user_id = 1
        self.assertEqual(4,guarantor.validate_dto(o))
    def test_hash_complete_yes(self):
        v = votation.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 1
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation.insert_votation_dto(v)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 5
        g.hash_ok = 1
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        guarantor.set_hash_ok(g.u.user_id,g.votation_id)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 6
        g.hash_ok = 1
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        guarantor.set_hash_ok(g.u.user_id,g.votation_id)
        self.assertTrue(guarantor.guarantors_hash_complete(v.votation_id))
    def test_hash_complete_no_1(self):
        v = votation.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 2
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation.insert_votation_dto(v)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 3
        g.hash_ok = 0
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 6
        g.hash_ok = 1
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        self.assertFalse(guarantor.guarantors_hash_complete(v.votation_id))
    def test_hash_complete_no_2(self):
        v = votation.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 2
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation.insert_votation_dto(v)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 1
        g.hash_ok = 1
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 3
        g.hash_ok = 0
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        self.assertFalse(guarantor.guarantors_hash_complete(v.votation_id))
    def test_insert_1(self):
        v = votation.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 2
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation.insert_votation_dto(v)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 1
        g.hash_ok = 1
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 3
        g.hash_ok = 0
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        ar = guarantor.load_guarantor_by_votation(v.votation_id)
        self.assertEqual(1,ar[0].order_n)
        self.assertEqual(2,ar[1].order_n)

    def test_load_1(self):
        v = votation.votation_dto()
        v.votation_description = 'Guar automated test ' + str(random.randint(1,500))
        v.votation_type = 'random'
        v.promoter_user.user_id = 2
        v.begin_date = '2018-01-01'
        v.end_date = '2018-01-15'
        v.votation_status = 1
        votation.insert_votation_dto(v)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 1
        g.hash_ok = 1
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        g = guarantor.guarantor_dto()
        g.votation_id = v.votation_id
        g.u.user_id = 3
        g.hash_ok = 0
        g.passphrase_ok = 0
        guarantor.insert_dto(g)
        g1 = guarantor.load_guarantor(v.votation_id, g.u.user_id)
        self.assertEqual(g.votation_id, g1.votation_id)
        self.assertEqual(g.u.user_id , g1.u.user_id )
        self.assertEqual(g.hash_ok , g1.hash_ok )
        self.assertEqual(g.passphrase_ok , g1.passphrase_ok )


if __name__ == '__main__':
    unittest.main()
