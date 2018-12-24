#!/usr/bin/env python3
import unittest
import option

class option_test(unittest.TestCase):
    def test_insert(self):
        option.delete_options_by_votation(999)
        u = option.option_dto()
        u.votation_id = 999
        u.option_name = 'test.option'
        u.description = 'test.description'
        option.insert_dto(u)
        ar = option.load_options_by_votation(u.votation_id)
        self.assertEqual(1,len(ar))
        u1 = ar[0]
        self.assertIsNotNone(u1)
        self.assertEqual(u.votation_id, u1.votation_id)
        self.assertEqual(u.option_name, u1.option_name)
        self.assertEqual(u.description, u1.description)
        option.delete_dto(u1)
        ar = option.load_options_by_votation(u.votation_id)
        self.assertEqual(0,len(ar))

    def test_text_ok(self):
        option.delete_options_by_votation(999)
        u = option.option_dto()
        self.assertTrue(option.save_options_from_text(999,"""test row 1
        test row 2
        test row 3""") )
        ar = option.load_options_by_votation(999)
        self.assertEqual(3, len(ar))
        self.assertEqual("TEST ROW 1", ar[0].option_name)
        self.assertEqual("TEST ROW 2", ar[1].option_name)
        self.assertEqual("TEST ROW 3", ar[2].option_name)
        option.delete_options_by_votation(999)

    def test_text_empty(self):
        option.delete_options_by_votation(999)
        u = option.option_dto()
        self.assertTrue( option.save_options_from_text(999,"""test row 1

        test row 2

        test row 3
        
        """) )
        ar = option.load_options_by_votation(999)
        self.assertEqual(3, len(ar))
        self.assertEqual("TEST ROW 1", ar[0].option_name)
        self.assertEqual("TEST ROW 2", ar[1].option_name)
        self.assertEqual("TEST ROW 3", ar[2].option_name)
        option.delete_options_by_votation(999)

    def test_text_duplicates(self):
        option.delete_options_by_votation(999)
        u = option.option_dto()
        self.assertTrue( option.save_options_from_text(999,"""test row 3
        test row 2
        test row 3
        test row 1
        """) )
        ar = option.load_options_by_votation(999)
        self.assertEqual(3, len(ar))
        self.assertEqual("TEST ROW 1", ar[0].option_name)
        self.assertEqual("TEST ROW 2", ar[1].option_name)
        self.assertEqual("TEST ROW 3", ar[2].option_name)
        option.delete_options_by_votation(999)




if __name__ == '__main__':
    unittest.main()
