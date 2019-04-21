#!/usr/bin/env python3
import unittest
import vote
import votation
import vote_maj_jud
import vote_simple

class vote_test(unittest.TestCase):
    def test_insert(self):
        vote.delete_votes_by_key("vote_key123")
        u = vote.vote_dto()
        u.vote_key = "vote_key123"
        u.votation_id = 999
        u.option_id = 123
        u.jud_value = 5
        vote.insert_dto(u)
        ar = vote.load_vote_by_key("vote_key123")
        self.assertEqual(1,len(ar))
        u1 = ar[0]
        self.assertIsNotNone(u1)
        self.assertEqual(u.votation_id, u1.votation_id)
        self.assertEqual(u.vote_key, u1.vote_key)
        self.assertEqual(u.option_id, u1.option_id)
        self.assertEqual(u.jud_value, u1.jud_value)
        vote.delete_votes_by_key("vote_key123")
        ar = vote.load_vote_by_key("vote_key123")
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
        vote.delete_votes_by_votation_id(999)
        u = vote.vote_dto()
        u.votation_id = 999
        u.option_id = 1001
        for i in range(10):
            u.vote_key = "vote_key1_" + str(i)
            u.jud_value = 1
            vote.insert_dto(u)
        for i in range(20):
            u.vote_key = "vote_key2_" + str(i)
            u.jud_value = 3
            vote.insert_dto(u)
        self.assertEqual([0,10,0,20,0,0], vote_maj_jud.count_votes_by_option(999,1001))
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
        self.assertTrue( vote_simple.save_vote(2,"akey",1234,10) )
        # check for duplicate key error:
        self.assertTrue( vote_simple.save_vote(2,"akey",1234,10) ) 


if __name__ == '__main__':
    unittest.main()

